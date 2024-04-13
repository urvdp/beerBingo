from fpdf.enums import XPos, YPos

from fpdf import fpdf

import numpy as np

from datetime import date, timedelta


class SPZPDF(fpdf.FPDF):
    def __init_(self, *args, **kwargs):
        super(SPZPDF, self).__init__(orientation='L', unit='mm', format='A4', font_cache_dir='/tmp')
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', uni=True)


class CertificateGenerator(SPZPDF):
    def header(this):
        this.width = 40
        this.height = 10

        this.set_font('Helvetica', '', size=36)

    def generateSheet(this, boxes, scale):
        # font size setting of the page
        boxes = randomize(boxes)
        this.set_margin(0)
        this.set_font('Helvetica', '', size=32)
        this.set_font(style="B")
        # self.pdf.set_font(style="U")
        length = 40
        border = 1
        this.set_y(20)
        this.cell(200, 10, "Beer Bingo", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        this.set_font('Helvetica', 'B', size=16)
        this.set_xy(10, this.y + 20)
        this.cell(200, 10, "Drinking sheet by:", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        this.set_y(70)
        # creation of first row with 5 categories
        this.set_x(20)
        index = 0
        for r_i in range(scale):
            for c_i in range(scale):
                this.multi_cell(length, length, boxes[index],
                                border=border, align="C", new_x="RIGHT", new_y="TOP", max_line_height=10)
                index += 1
            this.set_left_margin(20)
            this.set_y(this.y + length)

        this.set_y(this.y + 25)
        this.set_font('Helvetica', '', size=16)
        this.cell(200, 10, "I will have a hangover on " + str(date.today()+timedelta(days=1)) + "...    yeah :)")
        this.add_page()

    def generateDocument(this, categories, num, scale):

        for index in range(num):
            this.generateSheet(categories, scale)

        this.output("Beer_Bingo_{0}x{1}.pdf".format(scale, scale))


def randomize(dict):
    array = []
    array = dict
    np.random.shuffle(array)
    return array


if __name__ == '__main__':
    # put in the categories that should be shuffled
    categories = [
        "CHEERS!",
        "WHEAT",
        "DARK",
        "LIGHT",
        "PILSNER",
        "I don't really like beer, but I like this!",
        "TALL GUY (0.5l)",
        "BITTER",
        "SWEET",
        "Oetti",
        "MUG CLUB",
        "WINTER",
        "ALE",
        "Tannenzäpfle",
        "HOEPFNER",
        "SLOW BEER"
    ]

    # config

    number_of_sheets = 10
    # scaling factor, put 4 for 4x4 = 16 squares or 3 for 3x3 = 9 squares
    scaling = 4

    # generating code
    if len(categories) < scaling * scaling:
        print("There are not enough categories given for the number of boxes. Add "
              + str(scaling * scaling - len(categories)) + " categories to create a pdf sheet.")
    else:
        pdfGen = CertificateGenerator()
        pdfGen.add_page()
        pdfGen.generateDocument(categories, number_of_sheets, scaling)
