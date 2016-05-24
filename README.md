# fast.com
Python CLI-tool (without need for a GUI) to measure Internet speed with fast.com

Example output:

```
Loop 0 Total MB 20 Delta MB 20 Speed kB/s: 6933 aka Mbps 56.4
Loop 1 Total MB 57 Delta MB 37 Speed kB/s: 12700 aka Mbps 103.3
Loop 2 Total MB 65 Delta MB 7 Speed kB/s: 2633 aka Mbps 21.4
Loop 3 Total MB 74 Delta MB 9 Speed kB/s: 3300 aka Mbps 26.9
Loop 4 Total MB 75 Delta MB 0 Speed kB/s: 33 aka Mbps 0.3
Loop 5 Total MB 75 Delta MB 0 Speed kB/s: 0 aka Mbps 0.0
Done
Highest Speed (kB/s): 12700 aka Mbps 103.3

```

You need js-beautifier
```
sudo pip install jsbeautifier`
```

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

