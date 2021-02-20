# PlayUpgradeAssistant
Play Framework Massive Source Code Editing Facilities
20 Feb 2020
manabu@wingumd.com

## Why I Wrote This

Each play framework upgrade requires a massive amount of code changes as they obsolete some calls and 
completely remove some calls and often change the approach completely like requiring to add
the Http request as controller parameters or changes the way functions are called drastically.

Here is an example,

We had in our html template code

session.get("field")

This had to be changed to

req.session().getOrElse("field", "")

These also had to be done only on templates that did require the session. 

These changes cannot easily be done with text editor's find and replace and there will be a massive list
of files that need to be dealt with.

## What This Is

This has some useful facilities to help you write massive auto-editing. This *IS NOT* an auto-upgrade product,
but this is a "kit" with parts you can assemble to accomplish your specific upgrade work. 

Each new upgrade, I will leave behind some upgrade code I made, perhaps you can use most of these
codes to meet your own needs. But they are not written specific to your situation so carefully review the code.

## Why Python?

For this type of work, Python worked for me because,

* I can write if/then/else imperative editing code that's not easy with regular expressions only
* Simpler to set up, run and debug than Java or Scala
* With enough examples, most people even without Python experience can take this on.

I did think about providing elisp macros. I almost never use sed/awk so I don't know them.

## Facilities It Provides

### FileUtility

This assist you in loading files, load lines, stash away the original to somewhere just in case.

### LineUtility

This is the core of this kit. This support the following flow

* Find a function call you are targeting
* Extract the arguments

There is enough regular expression examples that you can expand (and hopefully contribute)

### TemplateFixer

This is an *Example* of what I did to our own code to add HTTP.Request throughout when needed
and edit session calls. You can see how the above facilities are used to accomplish them.

## Typical Workflow

I highly recommend the Unix type environment like MacOS or using Linux with WSL (Windows Subsystem for Linux)

1. Get The List of Target Files

Get the list of target files by first cd to the top of group of files like `views` or `controller`

* Unix
    find . > list.txt
  
* Windows
    dir /s > list.txt
  
1. Using the FileUtil and load the list and then process

Please check `main.py` on how these are done.

I highly recommend that you work on thee code changes by a new branch of your code base and while you 
experiment with the changes. I tylically need a full roll-back until the edits are completely tuned.










