#include <stdio.h>
#include <Python.h>


static PyObject * test_wrapper(PyObject * self, PyObject * args)
{
  // blocks are freed using LIFO strategy
  size_t n = 512-8;
  void * p1_again;

  void * p1 = PyObject_Malloc(n);
  void * p2 = PyObject_Malloc(n);
  void * p3 = PyObject_Malloc(n);
  // pool->ref.count=3;

  printf("p1: %p\np2: %p\np3: %p\n", p1, p2, p3);

  PyObject_Free(p1);
  // pool->ref.count=2; pool_header->freeblock = p1; p1->next=0;

  PyObject_Free(p1);
  // pool->ref.count=1; pool_header->freeblock = p1; p1->next=p1; 

  p1 = PyObject_Malloc(n);
  // pool->ref.count=2; pool_header->freeblock = p1; p1->next=p1;

  p1_again = PyObject_Malloc(n);
  // pool->ref.count=3;

  printf("p1: %p\np1_again: %p\n", p1, p1_again);

  PyObject * ret;
  ret = Py_BuildValue("i",0);
  return ret;
}

// register this function within a module’s symbol table (all Python functions live in a module, even if they’re actually C functions!)
static PyMethodDef HelloMethods[] = {
 { "test_free_method", (PyCFunction)test_wrapper, METH_VARARGS},
 { NULL, NULL, 0, NULL }
};

// write an init function for the module (all extension modules require an init function).
static struct PyModuleDef testfreePyDem =
{
  PyModuleDef_HEAD_INIT,
  "testfree", /* name of module */
  "",          /* module documentation, may be NULL */
  -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
  HelloMethods
};

// Note that the name of the PyMODINIT_FUNC function must be of the form PyInit_<name> where <name> is the name of your module.
PyMODINIT_FUNC PyInit_testfree(void) {
  return PyModule_Create(&testfreePyDem);
}
