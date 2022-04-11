# TheBigBrother
Prevents you from touching your face while you think, work or relax.

## Install
Run `./installer.sh -i` to install The Big Brother, and run `./installer.sh -r` for uninstalling it.

## Rationale
I needed a program that warned me every time I touch my beard while thinking, working or watching series.
After talking about this with some of my coworkers and friends I noticed that more people than I thought have the habit of unwillingly touch their beards, hair or even bite their hands or fingers while they think or work in front of the PC.
Thus I decided to create The Big Brother to help myself and people around me who suffer from the same problem or related ones.

## How does it work?
The Big Brother constantly watches you.  
It uses OpenCV and Mediapipe for hands and face detection in realtime.  
When it detects you're either going to touch your face or that you're actually doing it if run in default mode it will play the FBI siren until you stop.  
Otherwise The Big Brother supports the silent mode (enabled by passing `-s` to the executable) which works by covering your screen with a fullscreen window until you stop.  
The latter mode (even if a bit less effective) is very useful if you're going to use The Big Brother in your workplace or any other scenario where you can't have very loud sounds going off.  
The Big Brother is meant to be very annoying, and cause as much discomfort as possible when triggered. In fact it works by causing negative reinforcement.

## Usage
Just run The Big Brother at login or when you want really, if you need to touch your face for some reason like for example for adjusting your glasses you can hold the "Pause" or "Break" key on your keyboard and it won't trigger while you're holding it.
Run `bigbrother --help` for additional options.
