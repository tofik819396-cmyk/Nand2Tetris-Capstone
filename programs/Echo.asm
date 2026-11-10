// Echo.asm - Read KBD continuously and draw pixel blocks on Screen
(LOOP)
    @KBD
    D=M
    @NO_KEY
    D;JEQ

    // Key Pressed -> Fill first pixel row block (Screen RAM = -1)
    @SCREEN
    M=-1
    @LOOP
    0;JMP

(NO_KEY)
    // No Key -> Clear screen pixel block (Screen RAM = 0)
    @SCREEN
    M=0
    @LOOP
    0;JMP