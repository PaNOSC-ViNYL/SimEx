# Example geom file
# Line starting with "#" or ";" are ignored. ";" is compatible with CrystFEL files.

; [Geom]

; detector distance (m)
geom/d = 0.13

; pixel width (m)
geom/pix_width = 1400e-6

; number of pixels along x
geom/px = 101
# distance 0.13m, 220e-6 pix_width and 380 pixels gives 4 Angstrom resolution

; bad pixel map (ascii)
#geom/badpixmap = /data/yoon/singfel/dataShrine1/badpixelmap.dat
