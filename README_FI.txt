---------------------------------------------------------------------README-----------------------------------------------------------------

This code aims to help visualize the referential of a satellite in orbit.

Firstly, the referential must be defined, and that can be done using the provided picture.
As such, the X, Y, Z system is an orbital coordinate system with the Y axis along the instantaneous vertical
and the Z axis along the normal to the orbital plane and The x, y, z system is a set of body axes fixed in the vehicle and with an 
orientation relative to X, Y, Z specified by the angles alpha, beta and psi in pitch, roll and yaw respectively.

--------------------------------------------------------------------------------------------------------------------------------------------

When run, the program will first display a main window, with two options:

- In the section 'Evaluate Satellite', the user can input a satellite's moments of inertia. 
If the button 'Draw point' is pressed, according to the stability criteria explained in the report, the code will classify the 
satellite into a region of the Rx/Ry (or Kx/Ky).
If the button 'Display Image' is pressed, the code will provide a image with a 3D satellite's orientation, with Y being the vertical axis.

- In the section 'Design Satellite', the user can define the region of stability he wants its' satellite to be, by clicking on a point 
in the graph. Then, he must introduce JUST one of the three values of moments of inertia. When he presses 'Calculate I's', the program
will determine the other moments of inertia.

--------------------------------------------------------------------------------------------------------------------------------------------

The code is fully implemented, with 'Go Back' buttons to navigate between menus. Please mind that, in order to quit the program, the user
must press 'Quit program' on the main menu. Otherwise, the main window will keep on opening.

--------------------------------------------------------------------------------------------------------------------------------------------

NOTE: The code developed a bug in the final stages of development. So, we kindly ask for the user, when he generates a image, NOT to press
'Go Back' or 'Quit program', but instead to close the window and restart the program.
