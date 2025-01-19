# 1. Git credentials
## Setting up name and email address
```
git config --global user.name "Nikolay"
git config --global user.email "my@example.com"
```
---
# 2. Creating a project
## Create a repository
```
git init
Initialized empty Git repository in C:/PP2Main/.git/
```

## Add the page to the repository
```
git add hello.html
warning: in the working copy of 'hello.html', LF will be replaced by CRLF the next time Git touches it
PS C:\PP2Main> git commit -m "Initial Commit"
[main d9a7ce1] Initial Commit
1 file changed, 1 insertion(+)
create mode 100644 hello.html
```
---
# 3. Checking the status of the repository
## Check the status of the repository
```
git status
On branch main
Your branch is ahead of 'origin/main' by 2 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```
---
# 4. Making changes

## Changing the “Hello, World” page
```
PS C:\PP2Main> git status
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   work/hello.html

no changes added to commit (use "git add" and/or "git commit -a")
```
---
# 5. Staging the changes

## Adding changes
```
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html

```
---
# 7. Committing the changes

## Committing changes

```
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is ahead of 'origin/main' by 3 commits.
#   (use "git push" to publish your local commits)
#
# Changes to be committed:
#       modified:   hello.html
#
```
```
added h1 tag
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html

PS C:\PP2Main\work> git commit
[main 130c378] added h1 tag
 1 file changed, 1 insertion(+), 1 deletion(-)
PS C:\PP2Main\work>
```
---
```
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 4 commits.
  (use "git push" to publish your local commits)   

nothing to commit, working tree clean
```
---

# 8. Changes, not files

## First Change: Adding default page tags

```
<html>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```

## Add this change
```
PS C:\PP2Main\work> git add hello.html
warning: in the working copy of 'work/hello.html', LF will be replaced by CRLF the next time Git touches it
```

## Second change: Add the HTML headers
```
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```

## Check the current status
```
git status
On branch main
Your branch is ahead of 'origin/main' by 4 commits.
  (use "git push" to publish your local commits)   

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html
```

## Commit

```
git commit -m "Added standard HTML page tags" 
[main bbefbe7] Added standard HTML page tags
 1 file changed, 5 insertions(+), 1 deletion(-)
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 5 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html

no changes added to commit (use "git add" and/or "git commit -a")
```

## Adding the second change

```
git add .
warning: in the working copy of 'work/hello.html', LF will be replaced by CRLF the next time Git touches it
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 5 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html
```

## Commit the second change
```
PS C:\PP2Main\work> git commit -m "Added HTML header"
[main d469c0d] Added HTML header
 1 file changed, 2 insertions(+)
```
---
# 9. History

```
PS C:\PP2Main\work> git log
commit d469c0ddddf0bd0f53c0f48f96b95c37742ec67b (HEAD -> main)
Author: Nikolay1 <2097nikola2097@gmail.com>
Date:   Sun Jan 19 13:05:24 2025 +0500

    Added HTML header

commit bbefbe713483fe1db6f4c3d3dbfa7ff0bd1ef256
Author: Nikolay1 <2097nikola2097@gmail.com>
Date:   Sun Jan 19 13:03:48 2025 +0500

    Added standard HTML page tags

commit 130c3788a452f030e8f31c3de6a86cd82b900eff
Author: Nikolay1 <2097nikola2097@gmail.com>
Date:   Sun Jan 19 12:53:30 2025 +0500

    added h1 tag

commit ee2fc57aec9df9baf7788630832a4a5e08fa6e3c
Author: Nikolay1 <2097nikola2097@gmail.com>
Date:   Sun Jan 19 12:48:39 2025 +0500

    Add folder

commit b5e51dc54be6569d371c70d87fab6c91ab3731d9
Author: Nikolay1 <2097nikola2097@gmail.com>
Date:   Sun Jan 19 12:44:22 2025 +0500

    Add githowto work

commit d9a7ce17731648904ba89dc4243db6c2228838b0
Author: Nikolay1 <2097nikola2097@gmail.com>
Date:   Sun Jan 19 12:42:23 2025 +0500

    Initial Commit
``` 

## One line history
```
PS C:\PP2Main\work> git log --oneline
d469c0d (HEAD -> main) Added HTML header
bbefbe7 Added standard HTML page tags
130c378 added h1 tag
ee2fc57 Add folder
b5e51dc Add githowto work
d9a7ce1 Initial Commit
```

## The ultimate format of the log

```
PS C:\PP2Main\work> git log --pretty=format:"%h %ad | %s%d [%an]" --date=short
d469c0d 2025-01-19 | Added HTML header (HEAD -> main) [Nikolay1]
bbefbe7 2025-01-19 | Added standard HTML page tags [Nikolay1]
130c378 2025-01-19 | added h1 tag [Nikolay1]
ee2fc57 2025-01-19 | Add folder [Nikolay1]
b5e51dc 2025-01-19 | Add githowto work [Nikolay1]
d9a7ce1 2025-01-19 | Initial Commit [Nikolay1]
```
---
# 10. Getting older versions

## Getting hashes of the previous commit

```
git log
d469c0d 2025-01-19 | Added HTML header (HEAD -> main) [Nikolay1]
bbefbe7 2025-01-19 | Added standard HTML page tags [Nikolay1]
130c378 2025-01-19 | added h1 tag [Nikolay1]
ee2fc57 2025-01-19 | Add folder [Nikolay1]
b5e51dc 2025-01-19 | Add githowto work [Nikolay1]
d9a7ce1 2025-01-19 | Initial Commit [Nikolay1]
```

```
git checkout d9a7ce1
Note: switching to 'd9a7ce1'.

You are in 'detached HEAD' state. You can look around, make experimental 
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.      

If you want to create a new branch to retain commits you create, you may 
do so (now or later) by using -c with the switch command. Example:       

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at d9a7ce1 Initial Commit
```

```hello.html``` consists ```Hello world```

Now hello.html consists 
```
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```
---
# 11. Tagging versions

## Creating a tag for the first version

```
PS C:\PP2Main\work> git tag v1
PS C:\PP2Main\work> git log
d469c0d 2025-01-19 | Added HTML header (HEAD -> main, tag: v1) [Nikolay1]
bbefbe7 2025-01-19 | Added standard HTML page tags [Nikolay1]
130c378 2025-01-19 | added h1 tag [Nikolay1]
ee2fc57 2025-01-19 | Add folder [Nikolay1]
b5e51dc 2025-01-19 | Add githowto work [Nikolay1]
d9a7ce1 2025-01-19 | Initial Commit [Nikolay1]
```

## Tags for previous versions

```
PS C:\PP2Main\work> git checkout v1^
D       githowto.md
Note: switching to 'v1^'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at bbefbe7 Added standard HTML page tags
```

```hello.html``` consists

```
<html>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```

```
bbefbe7 2025-01-19 | Added standard HTML page tags (HEAD, tag: v1-beta) [Nikolay1]
130c378 2025-01-19 | added h1 tag [Nikolay1]
ee2fc57 2025-01-19 | Add folder [Nikolay1]
b5e51dc 2025-01-19 | Add githowto work [Nikolay1]
d9a7ce1 2025-01-19 | Initial Commit [Nikolay1]
```

## Check out by the tag name


```
PS C:\PP2Main\work> git checkout v1
D       githowto.md
Previous HEAD position was bbefbe7 Added standard HTML page tags
HEAD is now at d469c0d Added HTML header
PS C:\PP2Main\work> git checkout v1-beta
D       githowto.md
Previous HEAD position was d469c0d Added HTML header
HEAD is now at bbefbe7 Added standard HTML page tags
```

## Viewing tags with the tag command

```
PS C:\PP2Main\work> git tag
v1
v1-beta
```

## Viewing tags in logs

```
PS C:\PP2Main\work> git log main --all  
d469c0d 2025-01-19 | Added HTML header (tag: v1, main) [Nikolay1]
bbefbe7 2025-01-19 | Added standard HTML page tags (HEAD, tag: v1-beta) [Nikolay1]
130c378 2025-01-19 | added h1 tag [Nikolay1]
ee2fc57 2025-01-19 | Add folder [Nikolay1]
b5e51dc 2025-01-19 | Add githowto work [Nikolay1]
d9a7ce1 2025-01-19 | Initial Commit [Nikolay1]
```
---
# 12. Discarding local changes (before staging)

## Change hello.html

```
File: hello.html
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <!-- This is a bad comment. We want to revert it. -->
  </body>
</html>
```

## Check the status
```
PS C:\PP2Main\work> git status     
On branch main
Your branch is ahead of 'origin/main' by 6 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html

no changes added to commit (use "git add" and/or "git commit -a")
```

## Undoing the changes in the working directory

```
PS C:\PP2Main\work> git restore hello.html
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 6 commits.
  (use "git push" to publish your local commits)
```

Now ```hello.html``` consists

```
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```
---
# 13. Cancel staged changes (before committing)

## Edit file and stage changes

```
File: hello.html

<html>
  <head>
    <!-- This is an unwanted but staged comment -->
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>

```

```
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 6 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html
```

## Restore the staging area

``` PS C:\PP2Main\work> git restore --staged hello.html ```

## Restore the workign tree

```
git restore hello.html
PS C:\PP2Main\work> git status
On branch main
Your branch is ahead of 'origin/main' by 6 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```