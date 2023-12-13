---
layout: post
title: Plain text bug report navigation
author: Aaron Stacy
---

[Android bug reports](https://developer.android.com/studio/debug/bug-report)
contain a massive amount of information about what's happening on your device.
They're big, relatively poorly documented, and not easy to navigate. This post
has my notes on digging into a bug report in a text editor. A lot of the
information is generic to bug reports, but the copy/pastable bits are specific
to vim.

#### Why plain text?

I've seen some good web UIs for looking at bug reports, but if you're good with
your text editor, there are benefits:

* **Navigation between sections is really fast once you know what to search
  for**. If you spend a lot of time jumping around files in your text editor,
  it might be easier to stay in that mode when also navigating a bugreport.
* **[You can filter noise](#removefilter-lines)**. My workflow is frequently
  (a) find the crash, (b) search for related logs from the given app before
  that. Or maybe I just want to scan the log for what a given app has been
  doing. This gets really hard in a big report where there’s noise (i.e. gc
  notifications, chatty silencing, etc), so filtering these is an important
  feature to me…
* **Information is not lost**. Ever wonder what the different columns of the
  logcat lines mean? Unfortunately [the
  docs](https://source.android.com/setup/contribute/read-bug-reports#logcat)
  may be incorrect for the specific version of Android you’re bug reporting on.
  Bug report and logcat UIs frequently strip header information, but if you’re
  just looking at the text, the header includes the `logcat` command used,
  which can deterministically tell you what the columns are.

This guide is focused on some of the specifics of navigating the massive
bugreport text file, but for reference on how to identify different events, the
[Reading Bug
Reports](https://source.android.com/setup/contribute/read-bug-reports#history-focused-activities)
doc is very useful.

### Zip archive format

Typically bug reports are zip archives. Within that there’s a
`bugreport-<device code name>-<android build>.txt` file. That’s where all of
the interesting stuff is.

In vim, you can open the zip file, put your cursor on the `.txt` file and press
enter, and it’ll open that file.

### Logcat columns

```
Date  Time         UID    PID   TID  Lvl TAG
08-14 15:27:31.099 10161  3098  3098 W   ActivityThread: Failed to ...
```

### Get currently-running PIDs for package

You can find the package under `DUMP OF SERVICE CRITICAL cpuinfo` section, and
it’ll list all currently-running PIDs.

A lot of times you want info about crashed processes and when things started or
stopped, so you’ll want to look for the `am_proc_start` and `am_proc_died`
tags. If you’re curious what those numbers in there mean, [THE CODE IS THE
DOCUMENTATION](https://cs.android.com/android/platform/superproject/+/master:frameworks/base/services/core/java/com/android/server/am/ProcessList.java;l=2139;drc=2260bc18bd2e65b9adfe82cfbef2794ae6638e65).

For long-running processes, Event Log may not have the `am_proc_start` for a
given PID.

### Get package info

In the `DUMP OF SERVICE package` section, there’s a `Packages:` subsection. I
think you can usually just search `/\v^Packages:$` and there will only be one
line like this. Example:

```
Packages:
…
  Package [com.google.android.gms] (d25a194):
    userId=10161
    …
    lastUpdateTime=2020-08-14 15:25:11
    …
    declared permissions:
      com.google.android.gms.permission.INTERNAL_BROADCAST: prot=signature, INSTALLED
    …
    User 0: ceDataInode=5475 installed=true hidden=false suspended=false distractionFlags=0 stopped=false notLaunched=false enabled=0 instant=false virtual=false
    …
    User 10: ceDataInode=25088 installed=true hidden=false suspended=false distractionFlags=0 stopped=false notLaunched=false enabled=0 instant=false virtual=false
    …
```

#### Why does a package have multiple package info sections?

Note that anything on the system image will have 2 different packages with the
same package string, but different hashes. The first will have a
`lastUpdateTime` way in the past, and the second will have an
`installerPackageName=com.android.vending` and typically a more recent
`lastUpdateTime`.

### Remove/filter lines

A lot of times you want to find items related to a particular package, i.e.
com.google.android.gms, but if you just search for that string, you get a lot
of noise (i.e. `com.google.android.gms idenditcal 70 lines`). Removing these
lines makes it a lot easier to search for issues.

1. Optional: In your vimrc `set hlsearch | set incsearch` so that you can
   easily see if your search string is matching the lines you want to remove.
   And then you may want to `set nohlsearch | set noincsearch` if you're in an
   especially big report.
2. Optional: I also `nnoremap / /\v | vnoremap / /\v` so that by default
   searching for stuff uses not-arcane regex syntax.
3. Search for what you want to remove:

    ```
    /\vcom.google.android.gms identical.*lines<cr>
    ```

4. Remove those lines:

    ```
    :g/\vcom.google.android.gms identical.*lines/d<cr>
    ```

    Optionally, vim can auto-fill your last search by pressing `<c-r>/` after the first `/`:

    ```
    :g/<c-r>//d " `<c-r>/` gets replaced to the line above
    ```

    Or if you'd like the inverse, i.e. delete lines that don't match, throw a `!` in there:

    ```
    :g!/am_kill/d
    ```

### Find logs from a specific app

Once you’ve [gotten the UID for your app](#get-package-info), and [filtered the
noisy lines](#removefilter-lines), you can jump through the logs for your app
by searching for. So if you want to find log statements from UID 10161, you’d
search for a pattern of `<date> <time> 10161`.

It might help to start with the logcat section:

```
------ SYSTEM LOG (logcat -v threadtime -v printable -v uid -d *:v) ------
```

And then search for lines from the app:

```
/\v^\d+-\d+\s+\d+:\d+:\d+\.\d+\s+10161
```

### Google Play services noise I like to filter

There's a lot of noise I don't typically need, so the following might be
helpful to copy/paste and clean that up.

```
:g/\v 10161 .*GmsTraceAlert/d
:g/\v 10161 .*BlueskyManager/d
:g/\v 10161 .*chatty.*identical.*line/d
:g/\v 10161 .*ActivityThread.*Failed to find provider/d
```

### Combining logcat archives

Higher-end devices will sometimes archive logcat files. The files are numbered in the `FS/data/misc/logd` directory. I use this script to combine them into a single file for easier searching / navigation:

```shell
#!/bin/bash -e

br="$(python3 -c "import os; print(os.path.abspath(\"$1\"))")"
dir=$(dirname $br)
unzipped_dir=$dir/$(basename $br .zip)

if [ -e $unzipped_dir ]; then
  rm -rf $unzipped_dir
fi

mkdir $unzipped_dir
cd $unzipped_dir

unzip $br

if [ -e FS/data/misc/logd ]; then
  ls FS/data/misc/logd \
    | grep logcat \
    | grep -v .id \
    | sort -r \
    | sed 's|^|FS/data/misc/logd/|' \
    | xargs cat > combined_logcat.txt
fi
```

## Other resources

*   Official docs on [capturing bug
    reports](https://developer.android.com/studio/debug/bug-report).
*   Official docs on [reading bug
    reports](https://source.android.com/setup/contribute/read-bug-reports).
