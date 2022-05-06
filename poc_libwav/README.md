# CVE-2022-28488
The function wav_format_write in libwav.c in libwav through 2017-04-20 has an Use of Uninitialized Variable vulnerability. 


### Steps to reproduce the behavior
 - [POC](./POC)
 - compile the program with UndefinedBehaviorSanitizer
 - Run command: `./wav_gain POC /dev/null`


### Reference
- https://github.com/marc-q/libwav/issues/29
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28488


### Credits
0xrocky(z3r0x.r0cky@gmail.com)

g4rl337(4ckr0n@gmail.com)

tin-z(0v4rl0r5@gmail.com)


### Details

#### Asan report
```
Uninitialized bytes in __interceptor_fwrite at offset 0 inside [0x7ffed0df95e8, 16)
==273091==WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x2ca7dc in wav_chunk_write /dataZ/Part_2/libwav_example/libwav/tools/wav_gain/../../libwav.c
    #1 0x2cb559 in wav_write /dataZ/Part_2/libwav_example/libwav/tools/wav_gain/../../libwav.c:217:2
    #2 0x2cb559 in gain_file /dataZ/Part_2/libwav_example/libwav/tools/wav_gain/wav_gain.c:28:6
    #3 0x2cb559 in main /dataZ/Part_2/libwav_example/libwav/tools/wav_gain/wav_gain.c:43:3
    #4 0x7f6b850e10b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16
    #5 0x24b43d in _start (/dataZ/Part_2/libwav_example/libwav/Fuzzing/wav_gain+0x24b43d)

SUMMARY: MemorySanitizer: use-of-uninitialized-value /dataZ/Part_2/libwav_example/libwav/tools/wav_gain/../../libwav.c in wav_chunk_write
```

---

</br>

