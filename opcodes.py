"""
More info: https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
"""

opcodes = (
    (r'00ee'                                            , 'return;'             ),
    (r'00e0'                                            , 'disp_clear()'        ),
    (r'(?P<a>0[0-9a-f]{3})'                             , ''                    ),
    (r'1(?P<a>[0-9a-f]{3})'                             , 'goto 0x0{a};'        ),
    (r'2(?P<a>[0-9a-f]{3})'                             , '*(0x0{a})()'         ),
    (r'3(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'              , 'if(V{x}=={c})'       ),
    (r'4(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'              , 'if(V{x}!={c})'       ),
    (r'5(?P<x>[0-9a-f])(?P<y>[0-9a-f])0'                , 'if(V{x}==V{y})'      ),
    (r'6(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'              , 'V{x}={c}'            ),
    (r'7(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'              , 'V{x}+={c}'           ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])0'                , 'V{x}=V{y}'           ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])1'                , 'V{x}=V{x}|V{y}'      ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])2'                , 'V{x}=V{x}&V{y}'      ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])3'                , 'V{x}=V{x}^V{y}'      ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])4'                , 'V{x}+=V{y} '         ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])5'                , 'V{x}-=V{y}'          ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])6'                , 'V{x}>>=1'            ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])7'                , 'V{x}=V{y}-V{x}'      ),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])e'                , 'V{x}<<=1 '           ),
    (r'9(?P<x>[0-9a-f])(?P<y>[0-9a-f])0'                , 'if(V{x}!=V{y})'      ),
    (r'a(?P<a>[0-9a-f]{3})'                             , 'I=0x0{a}'            ),
    (r'b(?P<a>[0-9a-f]{3})'                             , 'PC=V0+0x0{a}'        ),
    (r'c(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'              , 'V{x}=rand()&{c}'     ),
    (r'd(?P<x>[0-9a-f])(?P<y>[0-9a-f])(?P<h>[0-9a-f])'  , 'draw(V{x},V{y},{h})' ),
    (r'e(?P<x>[0-9a-f])9e'                              , 'if(key()==V{x})'     ),
    (r'e(?P<x>[0-9a-f])a1'                              , 'if(key()!=V{x})'     ),
    (r'f(?P<x>[0-9a-f])07'                              , 'V{x} = get_delay()'  ),
    (r'f(?P<x>[0-9a-f])0a'                              , 'V{x} = get_key() '   ),
    (r'f(?P<x>[0-9a-f])15'                              , 'delay_timer(V{x})'   ),
    (r'f(?P<x>[0-9a-f])18'                              , 'sound_timer(V{x})'   ),
    (r'f(?P<x>[0-9a-f])1e'                              , 'I+=V{x}'             ),
    (r'f(?P<x>[0-9a-f])29'                              , 'I=sprite_addr[V{x}]' ),
    (r'f(?P<x>[0-9a-f])33'                              , 'set_BCD(V{x})'       ),
    (r'f(?P<x>[0-9a-f])55'                              , 'reg_dump(V{x},&I)'   ),
    (r'f(?P<x>[0-9a-f])65'                              , 'reg_load(Vx,&I)'     ),
)






