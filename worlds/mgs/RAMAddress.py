# Many values here aren't used as part of the Archipelago client, but are left in for those that are curious
class RAM:
    psx_MainRAM_memorysize = 2097152
    # 4D475300 = MGS.
    mgs_ROM_address = 0x10724 
    # 534C55535F3030352E39343B = SLUS_005.94; == disk_1
    # 534C55535F3030372E37363B = SLUS_007.76; == disk_2
    disk_number_address = 0x925C
    current_radio_value = 0xADDBC
    # Full oxygen is a value of 0x400
    current_oxygen_level = 0xAE1B4
    # Could be used to detect getting hit. Jumps from 0 to 7 then counts down after taking damge.
    redness_of_life_label = 0xADD78
    # Value of 0x2 when game is paused
    pause_indicator = 0xAE0A8
    current_health = 0xB752E
    current_health_alt = 0xB8C76 # use in helicopter rappel
    current_max_health = 0xB7530
    psyco_mantis_current_health = 0xB8CBE
    # starts at 0, if increased to any non-zero value 
    game_over_screen_counter = 0xADB4C # Non-zero value == Death
    # 2 bytes
    currently_equiped_item = 0xB7536
    # 0000 - Cigs - amount held at 0x0B7562 (FFFF or 0000 means does not have, 1 means has)
    # 0001 - Scope - amount held at 0x0B7564 (FFFF or 0000 means does not have, 1 means has)
    # 0002 - C.Box A - amount held at 0x0B7566 (FFFF or 0000 means does not have, 1 means has)
    # 0003 - C.Box B - amount held at 0x0B7568 (FFFF or 0000 means does not have, 1 means has)
    # 0004 - C.Box C - amount held at 0x0B756A (FFFF or 0000 means does not have, 1 means has)
    # 0005 - NVG - amount held at 0x0B756C (FFFF or 0000 means does not have, 1 means has)
    # 0006 - Therm G - amount held at 0x0B756E (FFFF or 0000 means does not have, 1 means has)
    # 0007 - Gasmask - amount held at 0x0B7570 (FFFF or 0000 means does not have, 1 means has)
    # 0008 - B. Armor - amount held at 0x0B7572 (FFFF or 0000 means does not have, 1 means has)
    # 0009 - Ketchup - amount held at 0x0B7574 (FFFF or 0000 means does not have, 1 means has)
    # 0010 - Stealth - amount held at 0x0B7576 (FFFF or 0000 means does not have, 1 means has)
    # 0011 - Bandana - amount held at 0x0B7578 (FFFF or 0000 means does not have, 1 means has)
    # 0012 - Camera - amount held at 0x0B757A (FFFF or 0000 means does not have, 1 means has)
    # 0013 - Ration - amount held at 0x0B757C (FFFF or 0000 means none. non-zero number means amount held. Any value above 07FF seems to break stuff)
    # 0014 - Medicine - amount held at 0x0B757E
    # 0015 - Diazepam - amount held at 0x0B7580
    # 0016 - Pal Key - amount held at 0x0B7582 (FFFF or 0000 means does not have, 1 means has)
    # 0017 - Lv. X Card - level held at 0x0B7584 (FFFF or 0000 means does not have, non-zero value is the current "level" of the keycard)
    # 0018 - Timer B (note, setting a value of 1 causes it to imediately explode and kill the player -- death link??) - time left until explosion at 0x0B7586
    # 0019 - Mine D - amount held at 0x0B7588 (FFFF or 0000 means does not have, 1 means has)
    # 0020 - Disc - amount held at 0x0B758A (FFFF or 0000 means does not have, 1 means has)
    # 0021 - Rope - amount held at 0x0B758C (FFFF or 0000 means does not have, 1 means has)
    # 0022 - Handker - amount held at 0x0B758E (FFFF or 0000 means does not have, 1 means has)
    # 0023 - Suppressor - amount held at 0x0B7590 (FFFF or 0000 means does not have, 1 means has)
    cigs_count_address = 0xB7562
    cigs_death_count_address = 0xB6C92
    scope_count_address = 0xB7564
    scope_death_count_address = 0xB6C94
    cbox_a_count_address = 0xB7566
    cbox_a_death_count_address = 0xB6C96
    cbox_b_count_address = 0xB7568
    cbox_b_death_count_address = 0xB6C98
    cbox_c_count_address = 0xB756A
    cbox_c_death_count_address = 0xB6C9A
    nvg_count_address = 0xB756C
    nvg_death_count_address = 0xB6C9C
    therm_g_count_address = 0xB756E
    therm_g_death_count_address = 0xB6C9E
    gasmask_count_address = 0xB7570
    gasmask_death_count_address = 0xB6CA0
    b_armor_count_address = 0xB7572
    b_armor_death_count_address = 0xB6CA2
    ketchup_count_address = 0xB7574
    ketchup_death_count_address = 0xB6CA4
    stealth_count_address = 0xB7576
    stealth_death_count_address = 0xB6CA6
    bandana_count_address = 0xB7578
    bandana_death_count_address = 0xB6CA8
    camera_count_address = 0xB757A
    camera_death_count_address = 0xB6CAA
    rations_count_address = 0xB757C
    rations_max_address = 0xB7592
    rations_death_count_address = 0xB6CAC
    # ration_temp_address = 0xB75A6 # E2E0 = Coldest value (stored at 0xB75A8)
    # ration_is_frozen_address = 0xB75A2 # 0001 = Frozen
    medicine_count_address = 0xB757E
    medicine_max_address = 0xB7594
    medicine_death_count_address = 0xB6CAE
    diazepam_count_address = 0xB7580
    diazepam_max_address = 0xB7596
    diazepam_death_count_address = 0xB6CB0
    pal_key_count_address = 0xB7582
    pal_key_death_count_address = 0xB6CB2
    pal_key_form_address = 0xB759A # 0000 = Normal, 0001 = Warm, 0002 = Cold.
    pal_key_temp_address = 0xB759C # 0000 = Normal, 2823 = Warmest value, DCD8 = Coldest Value (stored at 0xB75A0)
    cur_room_temp_address = 0xB7598 # 0000 = Normal, 001E = Warm, FFE2 = Cold
    key_card_count_address = 0xB7584
    key_card_death_count_address = 0xB6CB4
    time_bomb_count_address = 0xB7586
    time_bomb_death_count_address = 0xB6CB6
    mine_d_count_address = 0xB7588
    mind_d_death_count_address = 0xB6CB8
    disc_count_address = 0xB758A
    disc_death_count_address = 0xB6CBA
    rope_count_address = 0xB758C
    rope_death_count_address = 0xB6CBC
    handkerchief_count_address = 0xB758E
    handkerchief_death_count_address = 0xB6CBE
    suppressor_count_address = 0xB7590
    suppressor_death_count_address = 0xB6CC0
    
    # 2 bytes
    currently_equiped_weapon = 0xB7534
    # 0000 - SOCOM - ammo at 0x0B753A
    # 0001 - FAMAS - ammo at 0x0B753C
    # 0002 - Grenade - ammo at 0x0B753E
    # 0003 - Nikita - ammo at 0x0B7540
    # 0004 - Stinger - ammo at 0x0B7542
    # 0005 - Claymore - ammo at 0x0B7544
    # 0006 - C4 - ammo at 0x0B7546
    # 0007 - Stun. G - ammo at 0x0B7548
    # 0008 - Chaff G. - ammo at 0x0B754A
    # 0009 - PSG1 - ammo at 0x0B754C
    socom_ammo_address = 0xB753A
    socom_max_ammo_address = 0xB754E
    socom_death_ammo_address = 0xB6C6A
    famas_ammo_address = 0xB753C
    famas_max_ammo_address = 0xB7550
    famas_death_ammo_address = 0xB6C6C
    grenade_ammo_address = 0xB753E
    grenade_max_ammo_address = 0xB7552
    grenade_death_ammo_address = 0xB6C6E
    nikita_ammo_address = 0xB7540
    nikita_max_ammo_address = 0xB7554
    nikita_death_ammo_address = 0xB6C70
    stinger_ammo_address = 0xB7542
    stinger_max_ammo_address = 0xB7556
    stinger_death_ammo_address = 0xB6C72
    claymore_ammo_address = 0xB7544
    claymore_max_ammo_address = 0xB7558
    claymore_death_ammo_address = 0xB6C74
    c4_ammo_address = 0xB7546
    c4_max_ammo_address = 0xB755A
    c4_death_ammo_address = 0xB6C76
    stun_g_ammo_address = 0xB7548
    stun_g_max_ammo_address = 0xB755C
    stun_g_death_ammo_address = 0xB6C78
    chaff_g_ammo_address = 0xB754A
    chaff_g_max_ammo_address = 0xB755E
    chaff_g_death_ammo_address = 0xB6C7A
    psg1_ammo_address = 0xB754C
    psg1_max_ammo_address = 0xB7560
    psg1_death_ammo_address = 0xB6C7C

    # 2 bytes next to each other, seem to change somewhat independently (level and area?)
    # changing these values or freezing them doesn't seem to affect progression but they could be used to track it
    scene_tracker = 0xB7508
    # title // 0x6C746974 4 bytes
    # opening // 0x6E65706F 4 bytes
    # intro cutscene // 0x61303064 4 bytes
    # title.g
    # d00a..g // 3064 6130 0000 0067
    # S00a..g // 3073
    # d00a..g // 3064
    cutscene_text_address_primary = 0xBAAD4

    key_card_level_1_cutscene_bytes = b'Who...who, w' # I found it was easier to just copy the raw bytes rather than decode them to text first after doing it for this one
    key_card_level_2_cutscene_bytes = b'\x59\x6F\x75\x27\x72\x65\x20\x70\x72\x65\x74\x74'
    key_card_level_3_cutscene_bytes = b'\x57\x65\x6C\x6C\x2C\x20\x42\x6F\x73\x73\x2C\x20'
    key_card_level_4_cutscene_bytes = b'\x49\x20\x66\x65\x6C\x74\x20\x74\x68\x61\x74\x2C'
    key_card_level_5_cutscene_bytes = b'\x54\x68\x61\x74\x27\x73\x20\x74\x68\x65\x20\x73'
    key_card_level_6_cutscene_bytes = b'\x49\x74\x27\x73\x20\x6D\x65\x21\x00\x00\x00\x00'
    key_card_level_7_cutscene_bytes = b'\x4A\x75\x73\x74\x20\x61\x73\x20\x74\x68\x65\x20'

    boss_cutscene_bytes_to_location_list: dict[bytes, str] = {
        b'\x54\x68\x61\x6E\x6B\x73\x20\x66\x6F\x72\x20\x74': 'BOSS: Heavily Armed Genome Soldiers',
        b'\x59\x6F\x75\x27\x72\x65\x20\x70\x72\x65\x74\x74': 'BOSS: Revolver Ocelot', 
        b'\x57\x65\x6C\x6C\x2C\x20\x42\x6F\x73\x73\x2C\x20': 'BOSS: M1 Tank',
        b'\x49\x20\x66\x65\x6C\x74\x20\x74\x68\x61\x74\x2C': 'BOSS: Gray Fox',
        b'\x53\x6F\x2E\x2E\x2E\x79\x6F\x75\x20\x75\x73\x65': 'BOSS: Psycho Mantis',
        b'\x49\x74\x27\x73\x20\x68\x61\x72\x64\x20\x74\x6F': 'BOSS: Sniper Wolf I',
        b'\x49\x74\x27\x73\x20\x6D\x65\x21\x00\x00\x00\x00': 'Otacon Gifts',
        b'\x44\x61\x6D\x6E\x21\x21\x00\x00\x1C\x00\x00\x00': 'BOSS: Black-outfitted Genome Soldiers I',
        b'\x43\x27\x6D\x6F\x6E\x2C\x20\x66\x6C\x79\x21\x00': 'BOSS: A Hind D?',
        # 'BOSS: Stealth Camouflaged Genome Soldiers', # given when accessing snowfield for first time
        b'\x49\x2E\x2E\x2E\x00\x00\x00\x00\x18\x00\x00\x00': 'BOSS: Sniper Wolf II',
        b'\x57\x65\x6C\x63\x6F\x6D\x65\x2C\x20\x6B\x61\x73': 'BOSS: Black-outfitted Genome Soldiers II',
        b'\x4A\x75\x73\x74\x20\x61\x73\x20\x74\x68\x65\x20': 'BOSS: Vulcan Raven',
        b'\x53\x6E\x61\x6B\x65\x2C\x00\x00\x2C\x00\00\x00': 'BOSS: Metal Gear REX',
        b'\x53\x6E\x61\x61\x61\x61\x61\x61\x61\x61\x61\x6B': 'BOSS: Liquid Snake',
        b'\x4D\x65\x72\x79\x6C\x2C\x00\x00\x20\x00\x00\x00': 'The Best is Yet to Come'
    }
    # value at 0xAE098 + 0x150000 leads to address that holds area string 
    current_region_low_offset_address = 0xAE098
    current_region_high_offset_address = 0xAE09A

    # number of alerts triggered, 2 bytes
    alerts_triggered_count = 0xB75B4

    # number of continues used, 2 bytes
    continues_used_count = 0xB75C6