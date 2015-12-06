#All Downhill From Here

Grab your wax and your pointy hat - it's time to shred it up on the slopes. This challenge
 focuses on implementing a simple map editor that allows the user to create and edit their 
 own ski slope. The provided code allows the user to control a snowboarding elf. Courses 
 are loaded and saved as JSON files located in resources\courses.

#How it Works

##Game States

*MainMenu* Choose from playing or editing an existing course or creating a new one

*CourseSelectPlay* Select one of the existing courses to play

*Boarding* Hit the slopes

*CourseSelectEdit* Select an existing course to edit

*CourseInfoEntry* Allows the user to input the name and map size for a new course NOTE:
 For course names, dashes ("-") will be replaced by spaces (" ") to allow spaces in course
 names without spaces in the filename. 

*Editor* You will need to modify this class to allow the user to edit the course


##Obstacles

Trees, Rocks, Gates and Pylons are all collidable objects. If player.collider collides with
 obstacle.collider the player crashes.

##Collisions

Because of the map size and the number of objects involved (the included course is 5,000
 x 20,000 with 42,427 trees) trying to draw or handle collisions for all the objects would be
 abysmally slow. To get around this, I split the objects into a number of different "sections". 
 Sections are stored in a dict keyed by the (left, top, width, height) of the rect that each section 
 occupies on the map. Only sprites in sections whose rect collides with Course.view_rect are
 checked for collision detection.

##Drawing

The Course class contains a self.view_rect attribute which is a screen-sized rect centered on
 the player. Objects' draw methods take an offset argument so they are drawn in the correct
 position - any objects which collide with view_rect are drawn with
 (-view_rect.left, -view_rect.top) passed as the offset argument.

##Controls

*LEFT/RIGHT/DOWN* Change direction

*SPACE* "Brake" with the edge of the board

*F* Toggle fullscreen

*ESC* Exits the game from the main menu - returns user to the main menu from all other states

#Challenge

*Editor in Chief* Allow the user to edit course maps. This should be done using the provided Editor
 class (a subclass of state_engine.GameState). The user should be able to scroll the map and
 add/remove obstacles with the mouse. The provided code includes methods for loading and
 saving the edited course - make sure to call Editor.save_to_json before exiting the editor state.
 There is a spritesheet of semi-transparent icons for each of the object types if you want to go
 that route.

#Achievements

**Of the Essence** Implement and display a timer that tracks how long it takes the player to
 travel from the top lifthut to the bottom lifhut. The timer should reset for each run down the slope.

**Rocky Mountain Highs** Implement high score functionality that keeps track of the best times for
 each course. The best time for the course should be displayed along with the player's current time.
 Completing this achievement will also require completing Of the Essence. 

**Checkpoint Gnarly** In addition to keeping track of the total time to get down the mountain, keep
 track of how long it takes to reach certain checkpoints. Use these checkpoint times to compare the
 player's current run to the best time as they progress down the mountain. For example, if during
 the fastest run the player took 10 seconds to travel 1000 pixels down and during the current run
 the player passes the 1000px checkpoint in 9 seconds, the player's time vs. the leader would
 be -1.00 seconds. Completing this achievement will require completing the two previous achievements.

**Kriss Kross'll Make Ya** There is a Jump class in obstacles.py, but jumping is unimplemented.
 If the player is facing downhill when they hit a jump they should catch some air, not facing downhill
 should cause a crash. Completing this achievement will require modifications/additions to the
 Snowboarder and Jump classes.



