import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone

from prepoint import util as u

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

PREPOINT_LOGO = 'prepoint v0.1'
PREPOINT_LOGO_FONT = ('consolas', 20)
PREPOINT_SUB_LOGO = 'for local testing only'
PREPOINT_SUB_LOGO_FONT = ('consolas', 9)
MOVE_SCOPE_FONT = ('verdana bold', 12)
DEGREE_SIGN = 'deg'
# DEGREE_SIGN = u'\N{DEGREE SIGN}'
CHECK_MARK = '\u2714'  # unicode 'heavy check mark'
WRONG_MARK = '\u2718'  # unicode 'heavy ballot X'
NO_DATA = '---'


class ApplicationPrePoint(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # self.iconbitmap(self, default='pylcg-icon16.ico')  # must be an icon file
        tk.Tk.wm_title(self, 'prepoint  -- occultation pre-pointing tool in python 3')
        self.resizable(False, False)

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
        site_labelframe = tk.LabelFrame(left_frame, text=' Site ', padx=10, pady=10)
        site_labelframe.grid(pady=0, sticky='ew')
        site_inner_frame = tk.Frame(site_labelframe)
        site_inner_frame.pack()
        target_labelframe = tk.LabelFrame(left_frame, text=' Target ', padx=10, pady=10)
        target_labelframe.grid(pady=15, sticky='ew')
        # Populate site_labelframe:
        self.site_is_locked = False
        longitude_label = tk.Label(site_inner_frame, text='Long. ')
        longitude_label.grid(row=0, column=0, sticky='e')
        self.longitude = tk.StringVar()
        self.longitude.trace('w', self._update_site_area)
        self.longitude_entry = ttk.Entry(site_inner_frame, width=22, justify=tk.LEFT,
                                         textvariable=self.longitude)
        self.longitude_entry.grid(row=0, column=1, sticky='ew')
        self.longitude_ok_label = tk.Label(site_inner_frame, text=WRONG_MARK)
        self.longitude_ok_label.grid(row=0, column=2, sticky='ns')
        longitude_units_label = tk.Label(site_inner_frame, text=' ' + DEGREE_SIGN + '   +E -W')
        longitude_units_label.grid(row=0, column=3, sticky='w')
        latitude_label = tk.Label(site_inner_frame, text='Lat. ')
        latitude_label.grid(row=1, column=0, sticky='e')
        self.latitude = tk.StringVar()
        self.latitude.trace('w', self._update_site_area)
        self.latitude_entry = ttk.Entry(site_inner_frame, width=22, justify=tk.LEFT,
                                        textvariable=self.latitude)
        self.latitude_entry.grid(row=1, column=1, sticky='ew')
        self.latitude_ok_label = tk.Label(site_inner_frame, text=WRONG_MARK)
        self.latitude_ok_label.grid(row=1, column=2, sticky='ns')
        latitude_units_label = tk.Label(site_inner_frame, text=' ' + DEGREE_SIGN + '   +N -S')
        latitude_units_label.grid(row=1, column=3, sticky='w')

        site_lock_frame = tk.Frame(site_inner_frame)
        site_lock_frame.grid(row=2, column=0, columnspan=3, sticky='e')
        self.button_site_unlock = ttk.Button(site_lock_frame, text='Unlock',
                                             command=self._site_unlock_pressed)
        self.button_site_unlock.grid(row=0, column=0, sticky='ew')
        self.button_site_lock = ttk.Button(site_lock_frame, text='Lock', command=self.site_lock_pressed)
        self.button_site_lock.grid(row=0, column=1, sticky='ew')
        self._update_site_area()

        # Populate target_labelframe:
        target_ra_label = tk.Label(target_labelframe, text='RA ')
        target_ra_label.grid(row=0, column=0, sticky='e')
        self.target_ra = tk.StringVar()
        self.target_ra_entry = ttk.Entry(target_labelframe, width=16, justify=tk.LEFT,
                                         textvariable=self.target_ra)
        self.target_ra_entry.grid(row=0, column=1, sticky='e')
        self.target_ra_ok_label = tk.Label(target_labelframe, text=WRONG_MARK)
        self.target_ra_ok_label.grid(row=0, column=2, sticky='ns')
        target_ra_units_label = tk.Label(target_labelframe, text=' hh mm ss')
        target_ra_units_label.grid(row=0, column=3, sticky='w')
        target_dec_label = tk.Label(target_labelframe, text='Dec ')
        target_dec_label.grid(row=1, column=0, sticky='e')
        self.target_dec = tk.StringVar()
        self.target_dec_entry = ttk.Entry(target_labelframe, width=16, justify=tk.LEFT,
                                          textvariable=self.target_dec)
        self.target_dec_entry.grid(row=1, column=1, sticky='e')
        self.target_dec_ok_label = tk.Label(target_labelframe, text=WRONG_MARK)
        self.target_dec_ok_label.grid(row=1, column=2, sticky='ns')
        target_dec_units_label = tk.Label(target_labelframe, text=' ' + DEGREE_SIGN + '   +N -S')
        target_dec_units_label.grid(row=1, column=3, sticky='w')

        occ_time_label = tk.Label(target_labelframe, text='occ UTC ')
        occ_time_label.grid(row=2, column=0, sticky='e')
        self.occ_time = tk.StringVar()
        self.occ_time_entry = ttk.Entry(target_labelframe, width=14, justify=tk.LEFT,
                                        textvariable=self.occ_time)
        self.occ_time_entry.grid(row=2, column=1, sticky='e')
        self.occ_time_ok_label = tk.Label(target_labelframe, text=WRONG_MARK)
        self.occ_time_ok_label.grid(row=2, column=2, sticky='ns')
        occ_time_units_label = tk.Label(target_labelframe, text=' hh mm ss (next) ')
        occ_time_units_label.grid(row=2, column=3, sticky='w')
        target_lock_frame = tk.Frame(target_labelframe)
        target_lock_frame.grid(row=3, column=0, columnspan=3, sticky='e')
        self.button_target_unlock = ttk.Button(target_lock_frame, text='Unlock',
                                               command=self._unlock_target)
        self.button_target_unlock.grid(row=0, column=0, sticky='ew')
        self.button_target_lock = ttk.Button(target_lock_frame, text='Lock', command=self._lock_target)
        self.button_target_lock.grid(row=0, column=1, sticky='ew')

        # Populate right_frame:
        button_taking_image = ttk.Button(right_frame, text='\nCLICK when TAKING IMAGE\n',
                                         command=self._taking_image)
        button_taking_image.grid(sticky='ew')
        # self.image_time_text = tk.StringVar()
        self.label_image_time = tk.Label(right_frame, width=32, justify=tk.CENTER, text=NO_DATA)
        self.label_image_time.grid(sticky='ew')
        # self.image_time_text.set(NO_DATA)
        # Populate plate_solution_labelframe:
        plate_solution_labelframe = tk.LabelFrame(right_frame, text=' Enter Image PLATE SOLUTION: ',
                                                  padx=10, pady=10)
        plate_solution_labelframe.grid(pady=15, sticky='ew')
        plate_ra_label = tk.Label(plate_solution_labelframe, text='RA ')
        plate_ra_label.grid(row=0, column=0, sticky='e')
        self.plate_ra = tk.StringVar()
        plate_ra_entry = ttk.Entry(plate_solution_labelframe, width=16, justify=tk.LEFT,
                                   textvariable=self.plate_ra)
        plate_ra_entry.grid(row=0, column=1, sticky='ew')
        self.plate_ra_ok_label = tk.Label(plate_solution_labelframe, text=WRONG_MARK)
        self.plate_ra_ok_label.grid(row=0, column=2, sticky='ns')
        plate_ra_units_label = tk.Label(plate_solution_labelframe, text=' hh mm ss')
        plate_ra_units_label.grid(row=0, column=3, sticky='w')
        plate_dec_label = tk.Label(plate_solution_labelframe, text='Dec ')
        plate_dec_label.grid(row=1, column=0, sticky='e')
        self.plate_dec = tk.StringVar()
        plate_dec_entry = ttk.Entry(plate_solution_labelframe, width=16, justify=tk.LEFT,
                                    textvariable=self.plate_dec)
        plate_dec_entry.grid(row=1, column=1, sticky='ew')
        self.plate_dec_ok_label = tk.Label(plate_solution_labelframe, text=WRONG_MARK)
        self.plate_dec_ok_label.grid(row=1, column=2, sticky='ns')
        plate_dec_units_label = tk.Label(plate_solution_labelframe, text=' ' + DEGREE_SIGN + '   +N -S')
        plate_dec_units_label.grid(row=1, column=3, sticky='w')
        self.button_calc_moves = ttk.Button(plate_solution_labelframe, text='Calculate Required Moves',
                                            command=self._calc_and_display_moves)
        self.button_calc_moves.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.button_calc_moves.state(["disabled"])

        # Populate move_scope_labelframe:
        move_scope_labelframe = tk.LabelFrame(right_frame, text=' MOVE SCOPE ', font=MOVE_SCOPE_FONT,
                                              padx=10, pady=16)
        move_scope_labelframe.grid(pady=15, sticky='ew')
        self.left_right_label = tk.Label(move_scope_labelframe, text=NO_DATA, width=6, font=MOVE_SCOPE_FONT)
        self.left_right_label.grid(row=0, column=0, sticky='e')
        self.left_right_distance_label = tk.Label(move_scope_labelframe, text=NO_DATA, width=6,
                                                  font=MOVE_SCOPE_FONT)
        self.left_right_distance_label.grid(row=0, column=1, sticky='ew')
        self.left_right_degrees = tk.Label(move_scope_labelframe, text=NO_DATA, font=MOVE_SCOPE_FONT)
        self.left_right_degrees.grid(row=0, column=2, sticky='w')
        self.up_down_label = tk.Label(move_scope_labelframe, text=NO_DATA, width=6, font=MOVE_SCOPE_FONT)
        self.up_down_label.grid(row=1, column=0, sticky='e')
        self.up_down_distance_label = tk.Label(move_scope_labelframe, text=NO_DATA, width=6,
                                               font=MOVE_SCOPE_FONT)
        self.up_down_distance_label.grid(row=1, column=1, sticky='ew')
        self.up_down_degrees = tk.Label(move_scope_labelframe, text=NO_DATA, font=MOVE_SCOPE_FONT)
        self.up_down_degrees.grid(row=1, column=2, sticky='w')

    def _update_site_area(self, *keys):
        if self.site_is_locked:
            self.longitude_entry.state(["disabled"])
            self.latitude_entry.state(["disabled"])
            self.button_site_lock.state(["disabled"])
            self.button_site_unlock.state(['!disabled'])  # enabled
        else:
            longitude_is_valid = check_longitude_validity(self.longitude.get())
            latitude_is_valid = check_latitude_validity(self.latitude.get())
            set_validity_mark(self.longitude, check_longitude_validity, self.longitude_ok_label)
            set_validity_mark(self.latitude, check_latitude_validity, self.latitude_ok_label)
            if longitude_is_valid and latitude_is_valid:
                self.longitude_entry.state(["!disabled"])   # enabled
                self.latitude_entry.state(["!disabled"])    # enabled
                self.button_site_lock.state(["!disabled"])  # enabled
                self.button_site_unlock.state(['disabled'])
            else:
                self.longitude_entry.state(["!disabled"])   # enabled
                self.latitude_entry.state(["!disabled"])    # enabled
                self.button_site_lock.state(["disabled"])
                self.button_site_unlock.state(['disabled'])
        self._update_right_side()

    def site_lock_pressed(self):
        # if self.site_data_ok():
            self.button_site_unlock.state(['!disabled'])
            self.button_site_lock.state(['disabled'])
            self.site_data_locked = True

    def _site_unlock_pressed(self):
        self.button_site_unlock.state(['disabled'])
        self.button_site_lock.state(['!disabled'])
        self.site_data_locked = False

    def _lock_target(self):
        # if self.target_data_ok():
            self.button_target_unlock.state(['!disabled'])
            self.button_target_lock.state(['disabled'])
            self.target_data_locked = True

    def _unlock_target(self):
        self.button_target_unlock.state(['disabled'])
        self.button_target_lock.state(['!disabled'])
        self.target_data_locked = False

    def _taking_image(self):
        self.image_time = datetime.now(timezone.utc)
        self.label_image_time['text'] = 'taken  {:%Y-%m-%d %H:%M:%S}  UTC'.format(self.image_time)
        self._clear_move_data()

    def _calc_and_display_moves(self):
        """  The computational engine of this app."""
        az_current, alt_current = u.calc_az_alt(self.ra_plate, self.dec_plate,
                                                self.site_long, self.site_lat, self.image_time)
        az_occ, alt_occ = u.calc_az_alt(self.ra_occ, self.dec_occ,
                                        self.site_long, self.site_lat, self.occ_time)
        az_rightward = az_occ - az_current +\
                       (360 if (az_occ < az_current - 180) else 0)  # to cast into range [-180, +180].
        if az_rightward == 0:
            self.left_right_label['text'] = '(ok now)'
            self.left_right_distance_label['text'] = NO_DATA
            self.left_right_degrees['text'] = NO_DATA
        elif az_rightward < 0:
            self.left_right_label['text'] = 'LEFT'
            self.left_right_distance_label['text'] = '{:f20.6}'.format(abs(az_rightward)).strip()
            self.left_right_degrees['text'] = ' ' + DEGREE_SIGN
        else:
            self.left_right_label['text'] = 'RIGHT'
            self.left_right_distance_label['text'] = '{:f20.6}'.format(abs(az_rightward)).strip()
            self.left_right_degrees['text'] = ' ' + DEGREE_SIGN

        alt_upward = alt_occ - alt_current
        if alt_upward == 0:
            self.up_down_label['text'] = '(ok now)'
            self.up_down_distance_label['text'] = NO_DATA
            self.up_down_degrees['text'] = NO_DATA
        elif alt_upward < 0:
            self.up_down_label['text'] = 'LOWER'
            self.up_down_distance_label['text'] = '{:f20.6}'.format(abs(alt_upward)).strip()
            self.up_down_degrees['text'] = ' ' + DEGREE_SIGN
        else:
            self.up_down_label['text'] = 'RAISE'
            self.up_down_distance_label['text'] = '{:f20.6}'.format(abs(alt_upward)).strip()
            self.up_down_degrees['text'] = ' ' + DEGREE_SIGN

    def _clear_move_data(self):
        self.left_right_label['text'] = NO_DATA
        self.left_right_distance_label['text'] = NO_DATA
        self.left_right_degrees['text'] = NO_DATA
        self.up_down_label['text'] = NO_DATA
        self.up_down_distance_label['text'] = NO_DATA
        self.up_down_degrees['text'] = NO_DATA

    def _update_right_side(self):
        print('_update_right_side() called')


def set_validity_mark(control_variable, validity_function, label_to_set):
    """  Applies validity function to a control variable (Entry widget's current contents), and
         sets Label widget to X if not valid, check-mark if valid.
         validity of control_variable's content or not. """
    value = control_variable.get()
    is_valid = validity_function(value)
    character_to_write = CHECK_MARK if is_valid else WRONG_MARK
    label_to_set['text'] = character_to_write


def check_longitude_validity(longitude_text):
    allowed_chars = '0123456789+-: '
    if len(longitude_text.strip()) == 0 or (not all([c in allowed_chars for c in longitude_text])):
        return False
    longitude_degrees = u.hex_degrees_as_degrees(longitude_text)
    return -180 <= longitude_degrees <= +180


def check_latitude_validity(latitude_text):
    allowed_chars = '0123456789+-: '
    if len(latitude_text.strip()) == 0 or (not all([c in allowed_chars for c in latitude_text])):
        return False
    latitude_degrees = u.hex_degrees_as_degrees(latitude_text)
    return -90 <= latitude_degrees <= +90






# ***** Python file entry here. *****
# We must do without entry via functions, because tkinter just can't do that right.
# Thus, enter via this python file. We'll add arguments later, if necessary.
# Sigh.
# Well, at least this might later facilitate the making of executables for distribution.
if __name__ == "__main__":
    app = ApplicationPrePoint()
    app.mainloop()
