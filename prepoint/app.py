""" app.py
    Entry point for prepoint application."""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone

# import prepoint.util as u
import prepoint.util as u

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

PREPOINT_LOGO = 'prepoint v0.2 beta'
PREPOINT_LOGO_FONT = ('consolas', 20)
PREPOINT_SUB_LOGO = 'for testing only (E. Dose)'
PREPOINT_SUB_LOGO_FONT = ('consolas', 9)
MOVE_SCOPE_FONT = ('verdana bold', 12)
DEGREE_TEXT = 'deg'
DEGREE_SIGN = u'\N{DEGREE SIGN}'
CHECK_MARK = '\u2714'  # unicode 'heavy check mark'
WRONG_MARK = '\u2718'  # unicode 'heavy ballot X'
CHECK_WRONG_MARK_FONT = ('consolas', 11)
NO_DATA = '---'
CAMERA_ROTATION_TOLERANCE = 1.0  # degrees


class ApplicationPrePoint(tk.Tk):
    """ Main class for Tkinter. """
    def __init__(self):
        tk.Tk.__init__(self)
        # self.iconbitmap(self, default='pylcg-icon16.ico')  # must be an icon file
        tk.Tk.wm_title(self, 'prepoint  -- occultation pre-pointing tool in python 3')
        self.resizable(False, False)

        # Pre-declare variables needed for checking (avoid exceptions in code below):
        self.site_is_locked = False
        self.target_is_locked = False
        self.image_datetime = None
        self.plate_ra_degrees = None
        self.plate_dec_degrees = None

        # main_frame (fills entire application window):
        self.main_frame = tk.Frame(self)
        self.main_frame.grid()
        self.main_frame.pack(side="top", fill="both", expand=True)

        label_logo = tk.Label(self.main_frame, text=PREPOINT_LOGO,
                              font=PREPOINT_LOGO_FONT, fg='gray')
        label_logo.pack()
        label_logo = tk.Label(self.main_frame, text=PREPOINT_SUB_LOGO,
                              font=PREPOINT_SUB_LOGO_FONT, fg='black')
        label_logo.pack()
        body_frame = tk.Frame(self.main_frame)
        body_frame.pack()
        
        # Subdivide body_frame:
        left_frame = ttk.Frame(body_frame, padding=16)
        left_frame.grid(row=0, column=0, sticky='nsew')
        right_frame = ttk.Frame(body_frame, padding=16)
        right_frame.grid(row=0, column=1, sticky='ns')

        # Populate left_frame:
        site_labelframe = tk.LabelFrame(left_frame,
                                        text=' Observing site ', padx=10, pady=10)
        site_labelframe.grid(pady=0, sticky='ew')
        target_labelframe = tk.LabelFrame(left_frame,
                                          text=' Target star ', padx=10, pady=10)
        target_labelframe.grid(pady=15, sticky='ew')

        # Populate site_labelframe:
        self.site_is_locked = False
        site_inner_frame = tk.Frame(site_labelframe)
        site_inner_frame.pack()
        longitude_label = tk.Label(site_inner_frame, text='Long. ')
        longitude_label.grid(row=0, column=0, sticky='e')
        self.longitude = tk.StringVar()
        self.longitude.trace('w', self._update_site_area)
        self.longitude_entry = ttk.Entry(site_inner_frame, width=22, justify=tk.LEFT,
                                         textvariable=self.longitude)
        self.longitude_entry.grid(row=0, column=1, sticky='ew')
        self.longitude_ok_label = tk.Label(site_inner_frame,
                                           text=WRONG_MARK, font=CHECK_WRONG_MARK_FONT)
        self.longitude_ok_label.grid(row=0, column=2, sticky='ns')
        longitude_units_label = tk.Label(site_inner_frame,
                                         text=' ' + DEGREE_TEXT + '   +E  -W')
        longitude_units_label.grid(row=0, column=3, sticky='w')
        latitude_label = tk.Label(site_inner_frame, text='Lat. ')
        latitude_label.grid(row=1, column=0, sticky='e')
        self.latitude = tk.StringVar()
        self.latitude.trace('w', self._update_site_area)
        self.latitude_entry = ttk.Entry(site_inner_frame, width=22, justify=tk.LEFT,
                                        textvariable=self.latitude)
        self.latitude_entry.grid(row=1, column=1, sticky='ew')
        self.latitude_ok_label = tk.Label(site_inner_frame,
                                          text=WRONG_MARK, font=CHECK_WRONG_MARK_FONT)
        self.latitude_ok_label.grid(row=1, column=2, sticky='ns')
        latitude_units_label = tk.Label(site_inner_frame,
                                        text=' ' + DEGREE_TEXT + '   +N  -S')
        latitude_units_label.grid(row=1, column=3, sticky='w')

        site_readback_labelframe = tk.LabelFrame(site_inner_frame,
                                                 text=' readback ', padx=36, pady=5)
        site_readback_labelframe.grid(row=2, column=0, columnspan=4,
                                      sticky='ew', pady=6)
        site_readback_longitude_label = tk.Label(site_readback_labelframe,
                                                 text='Long. ')
        site_readback_longitude_label.grid(row=0, column=0, sticky='e')
        site_readback_latitude_label = tk.Label(site_readback_labelframe, text='Lat. ')
        site_readback_latitude_label.grid(row=1, column=0, sticky='e')
        self.site_readback_longitude_hex = tk.Label(site_readback_labelframe,
                                                    text=NO_DATA, padx=2)
        self.site_readback_longitude_hex.grid(row=0, column=1, sticky='e')
        self.site_readback_latitude_hex = tk.Label(site_readback_labelframe,
                                                   text=NO_DATA, padx=2)
        self.site_readback_latitude_hex.grid(row=1, column=1, sticky='e')
        self.site_readback_longitude_decimal = tk.Label(site_readback_labelframe,
                                                        text=NO_DATA, padx=2)
        self.site_readback_longitude_decimal.grid(row=0, column=2, sticky='e')
        self.site_readback_latitude_decimal = tk.Label(site_readback_labelframe,
                                                       text=NO_DATA, padx=2)
        self.site_readback_latitude_decimal.grid(row=1, column=2, sticky='e')

        site_lock_frame = tk.Frame(site_inner_frame)
        site_lock_frame.grid(row=3, column=0, columnspan=4, sticky='we')
        site_lock_frame.columnconfigure(0, weight=100)
        button_site_lock_frame_spacer = tk.Label(site_lock_frame, text=' ')
        button_site_lock_frame_spacer.grid(row=0, column=0, sticky='ew')
        self.button_site_unlock = ttk.Button(site_lock_frame, text='Unlock',
                                             command=self._site_unlock_pressed)
        self.button_site_unlock.grid(row=0, column=1, sticky='e')
        self.button_site_lock = ttk.Button(site_lock_frame, text='Lock',
                                           command=self.site_lock_pressed)
        self.button_site_lock.grid(row=0, column=2, sticky='e')
        self.locked_longitude_degrees = None
        self.locked_latitude_degrees = None
        self._update_site_area()

        # Populate target_labelframe:
        self.target_is_locked = False
        target_inner_frame = tk.Frame(target_labelframe)
        target_inner_frame.pack()

        target_ra_label = tk.Label(target_inner_frame, text='RA ')
        target_ra_label.grid(row=0, column=0, sticky='e')
        self.target_ra = tk.StringVar()
        self.target_ra.trace('w', self._update_target_area)
        self.target_ra_entry = ttk.Entry(target_inner_frame, width=22, justify=tk.LEFT,
                                         textvariable=self.target_ra)
        self.target_ra_entry.grid(row=0, column=1, sticky='ew')
        self.target_ra_ok_label = tk.Label(target_inner_frame,
                                           text=WRONG_MARK, font=CHECK_WRONG_MARK_FONT)
        self.target_ra_ok_label.grid(row=0, column=2, sticky='ns')
        target_ra_units_label = tk.Label(target_inner_frame, text=' hh mm ss')
        target_ra_units_label.grid(row=0, column=3, sticky='w')
        target_dec_label = tk.Label(target_inner_frame, text='Dec ')
        target_dec_label.grid(row=1, column=0, sticky='e')
        self.target_dec = tk.StringVar()
        self.target_dec.trace('w', self._update_target_area)
        self.target_dec_entry = ttk.Entry(target_inner_frame, width=22, justify=tk.LEFT,
                                          textvariable=self.target_dec)
        self.target_dec_entry.grid(row=1, column=1, sticky='ew')
        self.target_dec_ok_label = tk.Label(target_inner_frame,
                                            text=WRONG_MARK, font=CHECK_WRONG_MARK_FONT)
        self.target_dec_ok_label.grid(row=1, column=2, sticky='ns')
        target_dec_units_label = tk.Label(target_inner_frame,
                                          text=' ' + DEGREE_TEXT + '   +N  -S')
        target_dec_units_label.grid(row=1, column=3, sticky='w')

        occ_time_label = tk.Label(target_inner_frame, text='occ UTC ')
        occ_time_label.grid(row=2, column=0, sticky='e')
        self.occ_time = tk.StringVar()
        self.occ_time.trace('w', self._update_target_area)
        self.occ_time_entry = ttk.Entry(target_inner_frame, width=18, justify=tk.LEFT,
                                        textvariable=self.occ_time)
        self.occ_time_entry.grid(row=2, column=1, sticky='e')
        self.occ_time_ok_label = tk.Label(target_inner_frame,
                                          text=WRONG_MARK, font=CHECK_WRONG_MARK_FONT)
        self.occ_time_ok_label.grid(row=2, column=2, sticky='ns')
        occ_time_units_label = tk.Label(target_inner_frame, text=' hh mm ss (next) ')
        occ_time_units_label.grid(row=2, column=3, sticky='ew')

        target_readback_labelframe = tk.LabelFrame(target_inner_frame,
                                                   text=' readback ', padx=36, pady=5)
        target_readback_labelframe.grid(row=3, column=0, columnspan=4,
                                        sticky='ew', pady=6)
        target_readback_ra_label = tk.Label(target_readback_labelframe, text='RA ')
        target_readback_ra_label.grid(row=0, column=0, sticky='e')
        target_readback_dec_label = tk.Label(target_readback_labelframe, text='Dec ')
        target_readback_dec_label.grid(row=1, column=0, sticky='e')
        target_readback_occ_time_label = tk.Label(target_readback_labelframe,
                                                  text='occ UTC ')
        target_readback_occ_time_label.grid(row=2, column=0, sticky='e')
        target_readback_az_alt_label = tk.Label(target_readback_labelframe,
                                                text='AZ  ALT = ')
        target_readback_az_alt_label.grid(row=3, column=0, sticky='e')
        self.target_readback_ra_hex = tk.Label(target_readback_labelframe,
                                               text=NO_DATA, padx=2)
        self.target_readback_ra_hex.grid(row=0, column=1, sticky='e')
        self.target_readback_dec_hex = tk.Label(target_readback_labelframe,
                                                text=NO_DATA, padx=2)
        self.target_readback_dec_hex.grid(row=1, column=1, sticky='e')
        self.target_readback_occ_time = tk.Label(target_readback_labelframe,
                                                 text=NO_DATA, width=25, padx=2)
        self.target_readback_occ_time.grid(row=2, column=1, columnspan=2, sticky='e')
        self.target_readback_ra_decimal = tk.Label(target_readback_labelframe,
                                                   text=NO_DATA, padx=2)
        self.target_readback_ra_decimal.grid(row=0, column=2, sticky='e')
        self.target_readback_dec_decimal = tk.Label(target_readback_labelframe,
                                                    text=NO_DATA, padx=2)
        self.target_readback_dec_decimal.grid(row=1, column=2, sticky='e')
        self.target_readback_az = tk.Label(target_readback_labelframe,
                                           text=NO_DATA, padx=2)
        self.target_readback_az.grid(row=3, column=1, sticky='e')
        self.target_readback_alt = tk.Label(target_readback_labelframe,
                                            text=NO_DATA, padx=2)
        self.target_readback_alt.grid(row=3, column=2, sticky='e')

        target_lock_frame = tk.Frame(target_inner_frame)
        target_lock_frame.grid(row=4, column=0, columnspan=4, sticky='ew')
        target_lock_frame.columnconfigure(0, weight=100)
        button_target_lock_frame_spacer = tk.Label(target_lock_frame, text=' ')
        button_target_lock_frame_spacer.grid(row=0, column=0, sticky='ew')
        self.button_target_unlock = ttk.Button(target_lock_frame, text='Unlock',
                                               command=self._target_unlock_pressed)
        self.button_target_unlock.grid(row=0, column=1, sticky='e')
        self.button_target_lock = ttk.Button(target_lock_frame, text='Lock',
                                             command=self._target_lock_pressed)
        self.button_target_lock.grid(row=0, column=2, sticky='e')
        self.locked_target_ra_degrees = None
        self.locked_target_dec_degrees = None
        self.locked_occ_datetime = None
        self._update_target_area()

        # Populate right_frame:

        # Populate plate_solution_labelframe:
        plate_solution_labelframe = tk.LabelFrame(right_frame,
                                                  text=' From Image  -->'
                                                       ' Plate Solution ',
                                                  padx=10, pady=10)
        plate_solution_labelframe.grid(pady=5, sticky='ew')

        # Populate row 0 (frame of (button + time readout):
        taking_image_frame = ttk.Frame(plate_solution_labelframe, padding=2)
        taking_image_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
        taking_image_frame.columnconfigure(0, weight=100)
        button_taking_image = ttk.Button(taking_image_frame, width=26,
                                         text='\nCLICK when TAKING IMAGE\n',
                                         command=self._taking_image, padding=2)
        button_taking_image.grid(row=0, column=0, sticky='w')
        self.label_image_datetime = tk.Label(taking_image_frame, width=30,
                                             justify=tk.LEFT, text=NO_DATA)
        self.label_image_datetime.grid(row=0, column=1, sticky='w')
        self.image_datetime = None

        # Populate row 1 (subframe "taking_image_radec_frame" for (RA + Dec)):
        taking_image_radec_frame = ttk.Frame(plate_solution_labelframe, padding=5)
        taking_image_radec_frame.grid(row=1, column=0, columnspan=3,
                                      sticky='ew', pady=3)

        # Populate first row of subframe (RA):
        plate_ra_label = tk.Label(taking_image_radec_frame, text='RA ')
        plate_ra_label.grid(row=0, column=0, sticky='e')
        self.plate_ra = tk.StringVar()
        self.plate_ra.trace('w', self._update_plate_solution_area)
        plate_ra_entry = ttk.Entry(taking_image_radec_frame, width=24, justify=tk.LEFT,
                                   textvariable=self.plate_ra)
        plate_ra_entry.grid(row=0, column=1, sticky='ew')
        self.plate_ra_ok_label = tk.Label(taking_image_radec_frame, text=WRONG_MARK,
                                          font=CHECK_WRONG_MARK_FONT)
        self.plate_ra_ok_label.grid(row=0, column=2, sticky='ns')
        plate_ra_units_label = tk.Label(taking_image_radec_frame, text=' hh mm ss')
        plate_ra_units_label.grid(row=0, column=3, sticky='w')

        # Populate row 1 of subframe (Dec):
        plate_dec_label = tk.Label(taking_image_radec_frame, text='Dec ')
        plate_dec_label.grid(row=1, column=0, sticky='e')
        self.plate_dec = tk.StringVar()
        self.plate_dec.trace('w', self._update_plate_solution_area)
        plate_dec_entry = ttk.Entry(taking_image_radec_frame, width=24, justify=tk.LEFT,
                                    textvariable=self.plate_dec)
        plate_dec_entry.grid(row=1, column=1, sticky='ew')
        self.plate_dec_ok_label = tk.Label(taking_image_radec_frame, text=WRONG_MARK,
                                           font=CHECK_WRONG_MARK_FONT)
        self.plate_dec_ok_label.grid(row=1, column=2, sticky='ns')
        plate_dec_units_label = tk.Label(taking_image_radec_frame,
                                         text=' ' + DEGREE_TEXT + '   +N  -S')
        plate_dec_units_label.grid(row=1, column=3, sticky='w')

        # Populate row 2 (labelframe "readback"):
        plate_readback_labelframe = tk.LabelFrame(plate_solution_labelframe,
                                                  text=' readback ',
                                                  padx=36, pady=5)
        plate_readback_labelframe.grid(row=3, column=0, columnspan=4,
                                       sticky='ew', pady=3)
        plate_readback_ra_label = tk.Label(plate_readback_labelframe, text='RA ')
        plate_readback_ra_label.grid(row=0, column=0, sticky='e')
        plate_readback_dec_label = tk.Label(plate_readback_labelframe, text='Dec ')
        plate_readback_dec_label.grid(row=1, column=0, sticky='e')

        self.plate_readback_ra_hex = tk.Label(plate_readback_labelframe,
                                              text=NO_DATA, padx=2)
        self.plate_readback_ra_hex.grid(row=0, column=1, sticky='e')
        self.plate_readback_dec_hex = tk.Label(plate_readback_labelframe,
                                               text=NO_DATA, padx=2)
        self.plate_readback_dec_hex.grid(row=1, column=1, sticky='e')

        self.plate_readback_ra_decimal = tk.Label(plate_readback_labelframe,
                                                  text=NO_DATA, padx=2)
        self.plate_readback_ra_decimal.grid(row=0, column=2, sticky='e')
        self.plate_readback_dec_decimal = tk.Label(plate_readback_labelframe,
                                                   text=NO_DATA, padx=2)
        self.plate_readback_dec_decimal.grid(row=1, column=2, sticky='e')

        # Populate row 3 (button "Calculate Required Moves"):
        self.button_calc_moves = ttk.Button(plate_solution_labelframe,
                                            text='Calculate Required Moves',
                                            command=self._calc_and_display_moves)
        self.button_calc_moves.grid(row=4, column=1, columnspan=3, sticky='e')
        self.button_calc_moves.state(["disabled"])
        self.plate_ra_degrees = None
        self.plate_dec_degrees = None
        # self._update_plate_solution_area()

        # Populate row 4 "get_sharpcap_labelframe":
        get_sharpcap_labelframe = tk.LabelFrame(right_frame,
                                                text=' From SharpCap  --> clipboard ',
                                                padx=5, pady=5)
        get_sharpcap_labelframe.grid(row=4, column=0, columnspan=3, sticky='ew')
        get_sharpcap_button = ttk.Button(get_sharpcap_labelframe,
                                         text='GET SHARPCAP\nPlate Solution\n'
                                              'from clipboard', padding=6,
                                         command=self._get_sharpcap_platesolution)
        get_sharpcap_button.grid(row=0, column=0, rowspan=4, sticky='w',
                                 padx=14, ipadx=8, ipady=8)
        self.sharpcap_time_label = tk.Label(get_sharpcap_labelframe, text='')
        self.sharpcap_time_label.grid(row=0, column=1, sticky='e')
        self.sharpcap_time_value = tk.Label(get_sharpcap_labelframe, text=NO_DATA)
        self.sharpcap_time_value.grid(row=0, column=2, sticky='w')
        sharpcap_ra_label = tk.Label(get_sharpcap_labelframe, text='RA')
        sharpcap_ra_label.grid(row=1, column=1, sticky='e')
        self.sharpcap_ra_value = tk.Label(get_sharpcap_labelframe, text=NO_DATA)
        self.sharpcap_ra_value.grid(row=1, column=2, sticky='w')
        sharpcap_dec_label = tk.Label(get_sharpcap_labelframe, text='Dec')
        sharpcap_dec_label.grid(row=2, column=1, sticky='e')
        self.sharpcap_dec_value = tk.Label(get_sharpcap_labelframe, text=NO_DATA)
        self.sharpcap_dec_value.grid(row=2, column=2, sticky='w')
        sharpcap_rot_label = tk.Label(get_sharpcap_labelframe, text='Rotation')
        sharpcap_rot_label.grid(row=3, column=1, sticky='e')
        self.sharpcap_rot_value = tk.Label(get_sharpcap_labelframe, text=NO_DATA)
        self.sharpcap_rot_value.grid(row=3, column=2, sticky='w')

        # Populate row 5 "move_scope_labelframe":
        move_scope_labelframe = tk.LabelFrame(right_frame,
                                              text=' MOVE SCOPE ', font=MOVE_SCOPE_FONT,
                                              padx=10, pady=16)
        move_scope_labelframe.grid(pady=15, sticky='ew')
        self.left_right_label = tk.Label(move_scope_labelframe,
                                         text=NO_DATA, width=6, font=MOVE_SCOPE_FONT)
        self.left_right_label.grid(row=0, column=0, sticky='e')
        self.left_right_distance_label = tk.Label(move_scope_labelframe,
                                                  text=NO_DATA, width=6,
                                                  font=MOVE_SCOPE_FONT)
        self.left_right_distance_label.grid(row=0, column=1, sticky='ew')
        self.left_right_degrees = tk.Label(move_scope_labelframe,
                                           text=NO_DATA, font=MOVE_SCOPE_FONT)
        self.left_right_degrees.grid(row=0, column=2, sticky='w')
        self.up_down_label = tk.Label(move_scope_labelframe,
                                      text=NO_DATA, width=6, font=MOVE_SCOPE_FONT)
        self.up_down_label.grid(row=1, column=0, sticky='e')
        self.up_down_distance_label = tk.Label(move_scope_labelframe,
                                               text=NO_DATA, width=6,
                                               font=MOVE_SCOPE_FONT)
        self.up_down_distance_label.grid(row=1, column=1, sticky='ew')
        self.up_down_degrees = tk.Label(move_scope_labelframe,
                                        text=NO_DATA, font=MOVE_SCOPE_FONT)
        self.up_down_degrees.grid(row=1, column=2, sticky='w')

    # ============== SITE AREA =================

    # noinspection DuplicatedCode
    def _update_site_area(self, *keys):  # as in 2018 code.
        # def _update_site_area(self):
        if self.site_is_locked:
            self.longitude_entry.state(["disabled"])
            self.latitude_entry.state(["disabled"])
            self.button_site_lock.state(["disabled"])
            self.button_site_unlock.state(['!disabled'])  # enabled
        else:
            longitude_degrees = u.longitude_as_degrees(self.longitude.get())
            latitude_degrees = u.latitude_as_degrees(self.latitude.get())
            if longitude_degrees is None:
                self.longitude_ok_label['text'] = WRONG_MARK
                self.site_readback_longitude_hex['text'] = NO_DATA
                self.site_readback_longitude_decimal['text'] = NO_DATA
            else:
                self.longitude_ok_label['text'] = CHECK_MARK
                self.site_readback_longitude_hex['text'] = \
                    u.degrees_as_hex(longitude_degrees)
                self.site_readback_longitude_decimal['text'] = \
                    '{:10.5f}'.format(longitude_degrees) + DEGREE_SIGN
            if latitude_degrees is None:
                self.latitude_ok_label['text'] = WRONG_MARK
                self.site_readback_latitude_hex['text'] = NO_DATA
                self.site_readback_latitude_decimal['text'] = NO_DATA
            else:
                self.latitude_ok_label['text'] = CHECK_MARK
                self.site_readback_latitude_hex['text'] = \
                    u.degrees_as_hex(latitude_degrees)
                self.site_readback_latitude_decimal['text'] = \
                    '{:10.5f}'.format(latitude_degrees) + DEGREE_SIGN

            if longitude_degrees is None or latitude_degrees is None:
                # Can't use or lock Target data as entered.
                self.longitude_entry.state(["!disabled"])   # enabled
                self.latitude_entry.state(["!disabled"])    # enabled
                self.button_site_lock.state(["disabled"])
                self.button_site_unlock.state(['disabled'])
            else:
                # Site data as entered is valid and user may lock it.
                self.longitude_entry.state(["!disabled"])   # enabled
                self.latitude_entry.state(["!disabled"])    # enabled
                self.button_site_lock.state(["!disabled"])  # enabled
                self.button_site_unlock.state(['disabled'])

    def site_lock_pressed(self):
        """ When the Lock button for Site area is pressed. """
        self.longitude_entry.state(["disabled"])
        self.latitude_entry.state(["disabled"])
        self.locked_longitude_degrees = u.longitude_as_degrees(self.longitude.get())
        self.locked_latitude_degrees = u.latitude_as_degrees(self.latitude.get())
        self.button_site_unlock.state(['!disabled'])  # enabled
        self.button_site_lock.state(['disabled'])  # disabled
        self.site_is_locked = True
        self._update_calc_button()

    def _site_unlock_pressed(self):
        """ When the Unlock button for Site area is pressed. """
        self.longitude_entry.state(["!disabled"])
        self.latitude_entry.state(["!disabled"])
        self.button_site_unlock.state(['disabled'])  # disabled
        self.button_site_lock.state(['!disabled'])  # enabled
        self.site_is_locked = False
        self._update_calc_button()
        self._clear_move_data()

    # ============ TARGET_AREA ===============

    # noinspection DuplicatedCode
    def _update_target_area(self, *keys):  # as in 2018 code.
        # def _update_target_area(self):
        if self.target_is_locked:
            self.target_ra_entry.state(["disabled"])
            self.target_dec_entry.state(["disabled"])
            self.occ_time_entry.state(["disabled"])
            self.button_target_lock.state(["disabled"])
            self.button_target_unlock.state(['!disabled'])  # enabled
        else:
            ra_degrees = u.ra_as_degrees(self.target_ra.get())
            dec_degrees = u.dec_as_degrees(self.target_dec.get())
            occ_time = u.next_datetime_from_time_string(self.occ_time.get())
            if ra_degrees is None:
                self.target_ra_ok_label['text'] = WRONG_MARK
                self.target_readback_ra_hex['text'] = NO_DATA
                self.target_readback_ra_decimal['text'] = NO_DATA
            else:
                self.target_ra_ok_label['text'] = CHECK_MARK
                self.target_readback_ra_hex['text'] = u.ra_as_hours(ra_degrees)
                self.target_readback_ra_decimal['text'] = \
                    '{:10.5f}'.format(ra_degrees) + DEGREE_SIGN
            if dec_degrees is None:
                self.target_dec_ok_label['text'] = WRONG_MARK
                self.target_readback_dec_hex['text'] = NO_DATA
                self.target_readback_dec_decimal['text'] = NO_DATA
            else:
                self.target_dec_ok_label['text'] = CHECK_MARK
                self.target_readback_dec_hex['text'] = u.degrees_as_hex(dec_degrees)
                self.target_readback_dec_decimal['text'] = \
                    '{:10.5f}'.format(dec_degrees) + DEGREE_SIGN
            if occ_time is None:
                self.occ_time_ok_label['text'] = WRONG_MARK
                self.target_readback_occ_time['text'] = NO_DATA
            else:
                self.occ_time_ok_label['text'] = CHECK_MARK
                self.target_readback_occ_time['text'] = u.datetime_as_string(occ_time)

            if ra_degrees is None or dec_degrees is None or occ_time is None:
                # Can't use or lock Target data as entered.
                self.target_ra_entry.state(["!disabled"])  # enabled
                self.target_dec_entry.state(["!disabled"])  # enabled
                self.occ_time_entry.state(["!disabled"])  # enabled
                self.button_target_lock.state(["disabled"])
                self.button_target_unlock.state(['disabled'])
            else:
                # Site data as entered is valid and user may lock it.
                self.target_ra_entry.state(["!disabled"])  # enabled
                self.target_dec_entry.state(["!disabled"])  # enabled
                self.occ_time_entry.state(["!disabled"])  # enabled
                self.button_target_lock.state(["!disabled"])  # enabled
                self.button_target_unlock.state(['disabled'])

            if ra_degrees is None or dec_degrees is None or occ_time is None \
                    or (not self.site_is_locked):
                self.target_readback_az['text'] = NO_DATA
                self.target_readback_alt['text'] = NO_DATA
            else:
                az_occ, alt_occ = u.calc_az_alt(self.locked_longitude_degrees,
                                                self.locked_latitude_degrees,
                                                ra_degrees, dec_degrees, occ_time)
                self.target_readback_az['text'] = \
                    '{:7.2f}'.format(az_occ).strip() + DEGREE_SIGN
                self.target_readback_alt['text'] = \
                    '{:7.2f}'.format(alt_occ).strip() + DEGREE_SIGN

    def _target_lock_pressed(self):
        self.target_ra_entry.state(["disabled"])
        self.target_dec_entry.state(["disabled"])
        self.occ_time_entry.state(["disabled"])
        self.locked_target_ra_degrees = u.ra_as_degrees(self.target_ra.get())
        self.locked_target_dec_degrees = u.dec_as_degrees(self.target_dec.get())
        self.locked_occ_datetime = u.next_datetime_from_time_string(self.occ_time.get())
        self.button_target_unlock.state(['!disabled'])  # enabled
        self.button_target_lock.state(['disabled'])  # disabled
        self.target_is_locked = True
        self._update_calc_button()

    def _target_unlock_pressed(self):
        self.target_ra_entry.state(["!disabled"])
        self.target_dec_entry.state(["!disabled"])
        self.occ_time_entry.state(["!disabled"])
        self.button_target_unlock.state(['disabled'])  # disabled
        self.button_target_lock.state(['!disabled'])  # enabled
        self.target_is_locked = False
        self._update_calc_button()
        self._clear_move_data()

    # ============ IMAGE and PLATE SOLUTION AREA ===============

    def _taking_image(self):
        self.image_datetime = datetime.now(timezone.utc)
        self.label_image_datetime['text'] = \
            'image time =   ' + u.datetime_as_string(self.image_datetime)
        self._update_calc_button()
        self._clear_move_data()

    # noinspection DuplicatedCode
    def _update_plate_solution_area(self, *keys):  # as in 2018 code.
        # def _update_plate_solution_area(self):
        ra_degrees = u.ra_as_degrees(self.plate_ra.get())
        dec_degrees = u.dec_as_degrees(self.plate_dec.get())
        if ra_degrees is None:
            self.plate_ra_ok_label['text'] = WRONG_MARK
            self.plate_readback_ra_hex['text'] = NO_DATA
            self.plate_readback_ra_decimal['text'] = NO_DATA
        else:
            self.plate_ra_ok_label['text'] = CHECK_MARK
            self.plate_readback_ra_hex['text'] = u.ra_as_hours(ra_degrees)
            self.plate_readback_ra_decimal['text'] = \
                '{:10.5f}'.format(ra_degrees) + DEGREE_SIGN
        if dec_degrees is None:
            self.plate_dec_ok_label['text'] = WRONG_MARK
            self.plate_readback_dec_hex['text'] = NO_DATA
            self.plate_readback_dec_decimal['text'] = NO_DATA
        else:
            self.plate_dec_ok_label['text'] = CHECK_MARK
            self.plate_readback_dec_hex['text'] = \
                u.degrees_as_hex(dec_degrees)
            self.plate_readback_dec_decimal['text'] = \
                '{:10.5f}'.format(dec_degrees) + DEGREE_SIGN
        self.plate_ra_degrees = ra_degrees
        self.plate_dec_degrees = dec_degrees
        self._update_calc_button()
        self._clear_move_data()

    def _calc_and_display_moves(self):
        """  The computational engine of this app."""
        az_now, alt_now = u.calc_az_alt(self.locked_longitude_degrees,
                                        self.locked_latitude_degrees,
                                        self.plate_ra_degrees, self.plate_dec_degrees,
                                        self.image_datetime)
        az_occ, alt_occ = u.calc_az_alt(self.locked_longitude_degrees,
                                        self.locked_latitude_degrees,
                                        self.locked_target_ra_degrees,
                                        self.locked_target_dec_degrees,
                                        self.locked_occ_datetime)
        # Cast into range [-180, +180]:
        if az_occ < az_now - 180:
            az_rightward = az_occ - az_now + 360
        else:
            az_rightward = az_occ - az_now
        if az_rightward == 0:
            self.left_right_label['text'] = '(ok now)'
            self.left_right_distance_label['text'] = NO_DATA
            self.left_right_degrees['text'] = NO_DATA
        elif az_rightward < 0:
            self.left_right_label['text'] = 'LEFT'
            self.left_right_distance_label['text'] = \
                '{:10.2f}'.format(abs(az_rightward)).strip()
            self.left_right_degrees['text'] = ' ' + DEGREE_TEXT
        else:
            self.left_right_label['text'] = 'RIGHT'
            self.left_right_distance_label['text'] = \
                '{:10.2f}'.format(abs(az_rightward)).strip()
            self.left_right_degrees['text'] = ' ' + DEGREE_TEXT

        alt_upward = alt_occ - alt_now
        if alt_upward == 0:
            self.up_down_label['text'] = '(ok now)'
            self.up_down_distance_label['text'] = NO_DATA
            self.up_down_degrees['text'] = NO_DATA
        elif alt_upward < 0:
            self.up_down_label['text'] = 'LOWER'
            self.up_down_distance_label['text'] = \
                '{:10.2f}'.format(abs(alt_upward)).strip()
            self.up_down_degrees['text'] = ' ' + DEGREE_TEXT
        else:
            self.up_down_label['text'] = 'RAISE'
            self.up_down_distance_label['text'] = \
                '{:10.2f}'.format(abs(alt_upward)).strip()
            self.up_down_degrees['text'] = ' ' + DEGREE_TEXT

    def _clear_move_data(self):
        self.left_right_label['text'] = NO_DATA
        self.left_right_distance_label['text'] = NO_DATA
        self.left_right_degrees['text'] = NO_DATA
        self.up_down_label['text'] = NO_DATA
        self.up_down_distance_label['text'] = NO_DATA
        self.up_down_degrees['text'] = NO_DATA

    def _update_calc_button(self):
        # print('_update_calc_button() called')
        ready_to_calc = \
            self.site_is_locked and \
            self.target_is_locked and \
            self.image_datetime is not None and \
            self.plate_ra_degrees is not None and \
            self.plate_dec_degrees is not None
        if ready_to_calc:
            self.button_calc_moves.state(["!disabled"])  # enabled
        else:
            self.button_calc_moves.state(["disabled"])

    def _get_sharpcap_platesolution(self):

        # Get data needed to calculate moves:
        clipboard = u.get_windows_clipboard()
        return_tuple = u.parse_sharpcap_platesolution_text(clipboard)
        if return_tuple is None:
            self._clear_move_data()
            self.sharpcap_time_value['text'] = \
                'No SharpCap plate solution in clipboard.'
            return
        clipboard_datetime, self.plate_ra, self.plate_dec, self.plate_rotation = \
            return_tuple
        self.image_datetime = \
            u.datetime_as_string(clipboard_datetime).split('UTC')[0].strip()
        self.plate_ra_degrees = u.ra_as_degrees(self.plate_ra)
        self.plate_dec_degrees = u.dec_as_degrees(self.plate_dec)

        # Update SharpCap fields:
        self.sharpcap_time_value['text'] = self.image_datetime.strip() + '  UTC'
        self.sharpcap_ra_value['text'] = self.plate_ra
        self.sharpcap_dec_value['text'] = self.plate_dec
        sharpcap_rot_text = self.plate_rotation.strip() + DEGREE_SIGN
        sharpcap_abs_rot_text = sharpcap_rot_text[1:] \
            if sharpcap_rot_text.startswith('-') \
            else sharpcap_rot_text
        if float(self.plate_rotation) > CAMERA_ROTATION_TOLERANCE:
            camera_rotation_instruction = 'Turn camera CCW by ' + sharpcap_abs_rot_text
        elif float(self.plate_rotation) < -CAMERA_ROTATION_TOLERANCE:
            camera_rotation_instruction = 'Turn camera CW by ' + sharpcap_abs_rot_text
        else:
            camera_rotation_instruction = '(Do not turn camera.)'

        self.sharpcap_rot_value['text'] = \
            sharpcap_rot_text + ' --> ' + camera_rotation_instruction
        self._calc_and_display_moves()


# ***** Python file entry here. *****
# We must do without entry via functions, because tkinter just can't do that right.
# Thus, enter via this python file. We'll add arguments later, if necessary.
# Sigh.
# Well, at least this might later facilitate the making of executables for distribution.
if __name__ == "__main__":
    app = ApplicationPrePoint()
    app.mainloop()
