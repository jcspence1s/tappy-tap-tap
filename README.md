# tappy-tap-tap

Dependencies: 
Python3.6
pymata-aio

pymata-aio should auto detect arduino with StandardFirmata running. Pymata handles the serial interface to the firmata protocol.

Notes:
Large moves in the y-direction currently are bad, going back to origin (0, 0, -175ish) is typically fine. No notable bad things when moving in the x directions.
Cross is an acceptable input and will move the stylus in a cross pattern to the 4 reachable corners.
