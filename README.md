# ![Oiseau Logo](/OiseauLogoGitHub.png "Oiseau Logo")

Build Oct.22a, Build: ***Stable***

### How to install Oiseau:
#### Windows:
1. Download and run the setup file. ``OiseauSetup.exe``
2. Start Creating! Have fun with Oiseau!

#### Linux:
N/A at the moment. sorry.

# Getting Started:
## Hello Oiseau!
  Make a new folder, this is where our project will be located. Lets name it "New Folder". Lets create the main file, which will be called "main.oi".

Lets write the well-known "Hello World":
```javascript
  write "Hello World!";
```
In order to run it use the command `oiseau main.oi`
or go to the folder where the file is held and open it.
This should output:
```log
Hello World
```

## Group and Assign
After writing your first Oiseau Script you will need to learn how to store variables and make functions.
You make can make functions like so:
```javascript
  fun milk ~ () {};
```

This is a pretty bland function but since it doesn't have anything in it lets add a variable:
```javascript
  fun milk ~ () {
    coffee ~ "Perfectly done";
  };
```

Okay now that we know how to make functions lets run it!
This should output:
```log
```

Uh-oh it seems that we don't have a output.
Since we haven't ran our function or used the variable at all! Lets quickly do that.
You run functions like:
```javascript
  milk();
```

and for now you can use `#write coffee;` to print the current variable.
Your file should now look like:
```javascript
  fun milk ~ () {
    coffee ~ "Perfectly done";
    write coffee;
  };
  milk();
```
This should output:
```log
Perfectly done
```

# Beginner Concepts
## Conditions
Conditions (If you don't know already) are statements where the output only runs if the condition is true.
As a example lets set a condition so see if apples are red:
```javascript
apples ~ "red";
if apples == "red" {
  write "Apples are red";
};
``` 
If we run the file:
```log
Apples are red
```
Success!

Since we can do one lets do more ! 
```javascript
apples ~ "red";
if apples == "red" {
  write true;
};
if apples ~~ "blue" {
  write false;
};
if apples ~= "green" {
  write false;
};
```

As this would work as intended lets trim it a bit by replacing some of the if statements with a elif statement.
This makes the code cleaner and gets rid of unexepected outputs.

```javascript
apples ~ "red";
if apples == "red" {
  write true;
} elif apples == "blue" {
  write false;
} elif apples == "green" {
  write false;
};
```

The result should be:
```log
true
```

lets add a statement if none of those apply.
```javascript
apples ~ "red";
if apples == "red" {
  write true;
} elif apples == "blue" {
  write false;
} elif apples == "green" {
  write false;
} else {
  write "else achieved".
};
```

Similar to the if statement we have the while statement:
```javascript
while true {
  write "Hi";
};
```
but unlike the if statement you cannot chain them and they run until the condition isnt true anymore.
