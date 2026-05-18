# Try_projects
Come here when you want to try something. Let's try it together. They are children of wisdom.

<<<<<<< Updated upstream
---How to Use---
Please use this when you come up with an idea or decide to start a small-scale project.
・To get started, first create a branch with the temporary project name using a concise `firstcommit`.
・Please create a folder named Temporary Project Name. At this point, please explain the background of the project's inception.
This is the origin.
・Put your heart into it.
・As the project progresses and existing constraints start to get in the way,please spin off the project files into a new, independent repository.
Code below
<git clone 　original repository URL new-repo
=======
--How to Use---
Use this when you have an idea or decide to start a small project.

When creating a temporary project, create a folder and work within it.

You can separate branches if you don't want the history to get mixed with other projects, but the basic rule is to use `main`.

The first commit in a new temporary project
is the starting point.

• Work with passion.

• As the project progresses and existing constraints become a hindrance,
separate the project files into a new, independent repository.

The following code:
<git clone original repository URL new-repo
>>>>>>> Stashed changes
cd new-repo
git filter-repo --path src/moduleA --path-rename src/moduleA: --force

---Rules---
This is a test environment. Do not stay here forever.

• Do not create folders within each project.

• Do not merge branches or copy files from other branches.

• A single temporary project can only have a maximum of one branch.