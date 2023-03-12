# ![Oiseau Logo](/OiseauLogoGitHub.png "Oiseau Logo")

Build March.23b, Build: ***Stable***

### How to install Oiseau:
#### Windows:
1. Download and run the setup file. ``OiseauBuild.exe``
2. Start Creating! Have fun with Oiseau!

#### Linux:
N/A at the moment. sorry.

# Getting Started:
## Basics
On your computer, lets make a new folder, this is where our *basic* project will be located. Lets give it a very creative name: "Hello World Test". Within the folder, create a new file, this is where all the oiseau code will be stored. This file can have a few file extensions that will work with the interpreter: '.oi', '.ois' and '.ose'. Lets use the '.oi' extension and give it a very creative name "main.oi".

## Hello Oiseau!
Now that you have your file created lets put something in it.
Lets write the well-known, very famous "Hello World" using the 'write' keyword:
```javascript
  write "Hello World!";
```
Using this simple line of code we can now print things to the terminal, in this instance "Hello World!"

In order to run it use the command `oiseau main.oi` in the "Hello World Test" folder or go to the folder where the file is held and open it.
This should output:
```log
Hello World!
```

## Assigning and Grouping
Congrats you wrote your first Oiseau Program! You are on a track to learn the rest of the language. After writing your first Oiseau Script you will need to learn how to store variables and make functions.

Simple variables have two parts to it: the name and the value.
The name of the variable, aka the identifier, is any combination of a letter followed by more letters, numbers, underscores and hyphens.
The value is a bit more flexible as it can be any one of the datatypes listed below:

Boolean - using the two words exactly as written, 'true' and 'false', to say if the state is, well, true or false.

Decimal - as you can probably tell from the name, this datatype stores a decimal, this could be negitive or positive.

Empty - a datatype stating that the variable doesn't have a proper value.

Integer - as you can probably tell, again, from the name, this datatype stores a whole number, this could either be negitive or positive.

String - this data type can store any string of characters. Strings must be surrounded with double-quotes, if you want to use a double quote in your string you have to 
escape it using '\'. Example: "\"Example\""

Storage - this datatype can store any amount of the previously mentioned datatypes. thety have to be surrounded by the greater-than and less-than signs, aka '<' and '>'.

Using this knowledge we can now start making variables, you do it as shown here:
```javascript
  boolean ~ true;
  decimal ~ 3.14;
  empty_variable ~ empty;
  integer ~ 42;
  string ~ "Oiseau is pronounced Wa-zu";
  storage ~ <true, 3.14, empty, 42, "Oiseau is pronounced Wa-zu">
```

notice how '~' is used in these examples, this is one of the two basic assignment operators, the other one is the equal sign, '='. These can be used in the exace same environments as each other, use either one at your will.

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
