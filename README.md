# fast.com
Python CLI-tool (without need for a GUI) to measure Internet speed with fast.com


Example usage
```
$ python fast_com_example_usage.py 
Start speedtest against fast.com ...
Result: 53.4 Mbps
... Done
```

```
$ python
Python 2.7.6 (default, Jun 22 2015, 18:00:18) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import fast_com
>>> print fast_com.fast_com(maxtime=6)
55.6

```

Full verbose:
```
$ python fast_com.py
let's go:
javascript url is https://fast.com/app-ab2f99.js
token is YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm
https://ipv4_1-cxl0-c098.1.ams001.ix.nflxvideo.net/speedtest?c=nl&n=15435&v=3&e=1464113040&t=w0W6_z1NZauM49GMaogSm1d-ZTU
https://ipv4_1-cxl0-c073.1.ams001.ix.nflxvideo.net/speedtest?c=nl&n=15435&v=3&e=1464113040&t=Gq1NzaBpgH5zbSjLRRm7HlZ-v-o
https://ipv4_1-lagg0-c099.1.nyc001.ix.nflxvideo.net/speedtest?c=nl&n=15435&v=3&e=1464113040&t=kSYV0QidXeQe7otelqNwxd05R-w
Number of URLs: 3
Loop 0 Total MB 5 Delta MB 5 Speed kB/s: 2033 aka Mbps 16.5
Loop 1 Total MB 25 Delta MB 19 Speed kB/s: 6533 aka Mbps 53.2
Loop 2 Total MB 43 Delta MB 18 Speed kB/s: 6333 aka Mbps 51.5
Loop 3 Total MB 51 Delta MB 7 Speed kB/s: 2700 aka Mbps 22.0
Loop 4 Total MB 53 Delta MB 2 Speed kB/s: 733 aka Mbps 6.0
Loop 5 Total MB 55 Delta MB 1 Speed kB/s: 633 aka Mbps 5.2
Loop 6 Total MB 58 Delta MB 3 Speed kB/s: 1100 aka Mbps 9.0
Loop 7 Total MB 60 Delta MB 1 Speed kB/s: 500 aka Mbps 4.1
Highest Speed (kB/s): 6533 aka Mbps  53.2
done

```



