# Busy Light Indicator for Teams
Raspberry Pi 0/3/4 - connected to a RGB light. Color of light reflects Teams status (busy, free, away, presenting etc.)
A small LCD panel is also connected which shows a short message to re-enforce the light color.

There are two parts to the application:
1. Python API running on the RP3 that waits for status messages fromt he PC.
2. Python utility ont he PC that tracks the Teams status and calls the API accordingly.

![Teams Light](TeamsLight.jpg)
