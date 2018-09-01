# prepoint
#### a lightweight software tool to assist accurate pre-pointing of a non-tracking telescope for an upcoming star occultation event   

###### Eric Dose, New Mexico Mira Survey :: Albuquerque, NM

Say you want to capture a star occultation event, a short (e.g., 5-second) eclipsing of a star by a passing asteroid. Say also that you have the video camera to capture the event, a laptop to take the video and store it, and a telescope to gather the light into the video camera. Let's also say that you're not using a fixed-base, tracking telescope--you want the freedom to set up where you will, very useful for tracking these passing shadows which don't pass through your back yard all that often, but do quite often pass within short driving distance.  

So when you want to travel, or to set up in your back yard, then non-tracking telescopes like Dobsonians ("dobs") have some real advantages. They're light, they're easy to point, and they gather a LOT of light which helps get better results. But you do have to point them *in advance* to exactly where the occulted star *will be* when the asteroid passes in front.

This "pre-pointing" of your scope is as tricky as it sounds. You have to calculate where the star will be, you have to know how much time remains before the event, and you have to point the scope in the sky. Star hopping is hard enough with static objects, but when your sky position keeps changing as you're hunting through a finder scope, it's harder. And if you're traveling, then you're doing it all in probably unfamiliar terrain, and of course in the dark and probably sleep deprived. No place to be hex conversions or RA subtractions on the fly. It requires all sorts of skills that people are really bad at.

But computers are really good at them: they keep good time, do quick math without error, and don't care whether it's dark or cold or 4 in the morning. 

#### The Prepoint tool

So let me present a small Windows app that I think will help. See a screenshot: prepoint screenshot.png, in this repo. 

To use the tool, just work your way down the screenshot's left column, then down the right column. You occultation observers will get it right away.
 
1. Enter your observing location (longitude and latitude). Enter the event's predicted sky position and time (RA, Declination, UTC time). Enter angles in hex or decimal--the app will read back your entries in both. You can enter all this in advance, at your leisure. Click the Lock buttons so that you can't accidentally mess up these important data in the dark.
2. The AZ/ALT at bottom of the left column are where you point your scope. Just get it close--the next steps will refine your pointing. 
3. When the scope and video camera are set up, take a video frame long enough to get plenty of stars, and at the same time press the "Click when Taking Image" button to record the image's time.
4. Plate-solve the video frame with a plate solver (e.g., All-Sky Plate Solver), then enter its RA and Dec into the app. 
5. When all these data look good, click "Calculate Required Moves".
6. Move the telescope as directed in the "Move Scope" data box.
7. Repeat 3-6 if necessary for refinement or confirmation.



You can take your time with this tool. You just follow the Move Scope recommendations. It doesn't matter when you make the changes, as long as you make them sometime before you start your observation video for the occultation event itself. Especially ideal if you're setting up several scopes so that some must be prepointed hours in advance.

I'm offering this tool now (Sept 1 2018), as just completed. I have tested it against high-end planetarium software and agrees within 0.02 degrees (~ 5 seconds' sky movement). I cannot wait to test it for real under our next clear sky. 

Should you be interested in trying this out for yourself, contact me, Eric Dose, through Github. If there is some interest, I may make a Windows executable available.
