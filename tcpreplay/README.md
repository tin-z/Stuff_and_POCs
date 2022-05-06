# CVE-2022-28487
Tcpreplay version 4.4.1 contains a memory leakage flaw in fix_ipv6_checksums() function. The highest threat from this vulnerability is to data confidentiality. 


### Steps to reproduce the behavior
 - unknown


### Reference
- https://github.com/appneta/tcpreplay/issues/723
- https://github.com/appneta/tcpreplay/pull/720
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28487


### Credits
0xrocky(z3r0x.r0cky@gmail.com)

g4rl337(4ckr0n@gmail.com)

tin-z(0v4rl0r5@gmail.com)


### Details

https://github.com/appneta/tcpreplay/blob/09f07748dcabe3d58961f123f31dd0f75198a389/src/tcpedit/edit_packet.c#L160-L166


---

</br>

