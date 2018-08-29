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
        # site_inner_frame.grid(sticky=tk.E)
        target_labelframe = tk.LabelFrame(left_frame, text=' Target ', padx=10, pady=10)
        target_labelframe.grid(pady=15, sticky='ew')
        # Populate site_labelframe:
        longitude_label = tk.Label(site_inner_frame, text='Long. ')
        longitude_label.grid(row=0, column=0, sticky='e')
        longitude = tk.StringVar()
        longitude_entry = ttk.Entry(site_inner_frame, width=22, justify=tk.LEFT, textvariable=longitude)
        longitude_entry.grid(row=0, column=1, sticky='ew')
        longitude_label = tk.Label(site_inner_frame, text=' ' + DEGREE_SIGN + '   +E -W')
        longitude_label.grid(row=0, column=2, sticky='w')
        latitude_label = tk.Label(site_inner_frame, text='Lat. ')
        latitude_label.grid(row=1, column=0, sticky='e')
        latitude = tk.StringVar()
        latitude_entry = ttk.Entry(site_inner_frame, width=22, justify=tk.LEFT, textvariable=latitude)
        latitude_entry.grid(row=1, column=1, sticky='ew')
        latitude_label = tk.Label(site_inner_frame, text=' ' + DEGREE_SIGN + '   +N -S')
        latitude_label.grid(row=1, column=2, sticky='w')

        site_lock_frame = tk.Frame(site_inner_frame)
        site_lock_frame.grid(row=2, column=0, columnspan=3, sticky='e')
        self.button_site_unlock = ttk.Button(site_lock_frame, text='Unlock', command=self._unlock_site)
        self.button_site_unlock.grid(row=0, column=0, sticky='ew')
        self.button_site_lock = ttk.Button(site_lock_frame, text='Lock', command=self._lock_site)
        self.button_site_lock.grid(row=0, column=1, sticky='ew')
        self._unlock_site()

        # Populate target_labelframe:
        target_ra_label = tk.Label(target_labelframe, text='RA ')
        target_ra_label.grid(row=0, column=0, sticky='e')
        target_ra = tk.StringVar()
        target_ra_entry = ttk.Entry(target_labelframe, width=16, justify=tk.LEFT, textvariable=target_ra)
        target_ra_entry.grid(row=0, column=1, sticky='ew')
        target_ra_label = tk.Label(target_labelframe, text=' hh mm ss')
        target_ra_label.grid(row=0, column=2, sticky='w')
        target_dec_label = tk.Label(target_labelframe, text='Dec ')
        target_dec_label.grid(row=1, column=0, sticky='e')
        target_dec = tk.StringVar()
        target_dec_entry = ttk.Entry(target_labelframe, width=16, justify=tk.LEFT, textvariable=target_dec)
        target_dec_entry.grid(row=1, column=1, sticky='ew')
        target_dec_label = tk.Label(target_labelframe, text=' ' + DEGREE_SIGN + '   +N-S')
        target_dec_label.grid(row=1, column=2, sticky='w')

        occ_time_label = tk.Label(target_labelframe, text='occ UTC ')
        occ_time_label.grid(row=2, column=0, sticky='e')
        occ_time = tk.StringVar()
        occ_time_entry = ttk.Entry(target_labelframe, width=12, justify=tk.LEFT, textvariable=occ_time)
        occ_time_entry.grid(row=2, column=1, sticky='ew')
        occ_time_label = tk.Label(target_labelframe, text=' hh mm ss (next) ')
        occ_time_label.grid(row=2, column=2, sticky='w')
        target_lock_frame = tk.Frame(target_labelframe)
        target_lock_frame.grid(row=3, column=0, columnspan=3, sticky='e')
        self.button_target_unlock = ttk.Button(target_lock_frame, text='Unlock',
                                               command=self._unlock_target)
        self.button_target_unlock.grid(row=0, column=0, sticky='ew')
        self.button_target_lock = ttk.Button(target_lock_frame, text='Lock', command=self._lock_target)
        self.button_target_lock.grid(row=0, column=1, sticky='ew')
        self._unlock_target()

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
        plate_ra = tk.StringVar()
        plate_ra_entry = ttk.Entry(plate_solution_labelframe, width=16, justify=tk.LEFT,
                                   textvariable=plate_ra)
        plate_ra_entry.grid(row=0, column=1, sticky='ew')
        plate_ra_label = tk.Label(plate_solution_labelframe, text=' hh mm ss')
        plate_ra_label.grid(row=0, column=2, sticky='w')
        plate_dec_label = tk.Label(plate_solution_labelframe, text='Dec ')
        plate_dec_label.grid(row=1, column=0, sticky='e')
        plate_dec = tk.StringVar()
        plate_dec_entry = ttk.Entry(plate_solution_labelframe, width=16, justify=tk.LEFT,
                                    textvariable=plate_dec)
        plate_dec_entry.grid(row=1, column=1, sticky='ew')
        plate_dec_label = tk.Label(plate_solution_labelframe, text=' ' + DEGREE_SIGN + '   +N-S')
        plate_dec_label.grid(row=1, column=2, sticky='w')
        button_calc_moves = ttk.Button(plate_solution_labelframe, text='Calculate Required Moves',
                                       command=self._calc_and_display_moves)
        button_calc_moves.grid(row=2, column=1, columnspan=2, sticky='ew')
        button_calc_moves.state(["disabled"])

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

    def _lock_site(self):
        # if self.site_data_ok():
            self.button_site_unlock.state(['!disabled'])
            self.button_site_lock.state(['disabled'])
            self.site_data_locked = True

    def _unlock_site(self):
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
        az_rightward = az_occ - az_current + \
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


# ***** Python file entry here. *****
# We must do without entry via functions, because tkinter just can't do that right.
# Thus, enter via this python file. We'll add arguments later, if necessary.
# Sigh.
# Well, at least this might later facilitate the making of executables for distribution.
if __name__ == "__main__":
    app = ApplicationPrePoint()
    app.mainloop()
