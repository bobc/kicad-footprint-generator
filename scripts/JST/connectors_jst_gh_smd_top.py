    #!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from KicadModTree import *
from KicadModTree.nodes.base.Pad import Pad  # NOQA
from helpers import *
from math import sqrt

#parser = argparse.ArgumentParser()
#parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
#parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
#args = parser.parse_args()

# http://www.jst-mfg.com/product/pdf/eng/eGH.pdf

series = "GH"
orientation = 'Vertical'
number_of_rows = 1
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/eGH.pdf'

#pincount = int(args.pincount[0])
def generate_one_footprint(pincount, configuration):
    pad_edge_silk_center_offset = configuration['silk_pad_clearence'] + configuration['silk_line_width']/2

    pad_outside_y = 5.6
    pad_size = [0.6, pad_outside_y - 3.9]
    pad_spacing = 1.25
    mounting_pad_size = [1, 2.8]
    pad_to_mountpad = 1.35 + mounting_pad_size[0]/2

    p = 0.3

    A = (pincount - 1) * 1.25
    b_size_x = A + 4.5
    b_size_y = 4.25

    pad_y = pad_outside_y/2 - pad_size[1]/2

    mpad_x = -A/2 - pad_to_mountpad
    mpad_y = -pad_outside_y/2 + mounting_pad_size[1]/2


    # body outline coordinates
    oyt = -pad_outside_y/2 + p
    oyb = oyt + b_size_y
    oxl = -b_size_x/2
    oxr = b_size_x/2

    jst_name = "BM{pincount:02}B-GHS-TBT".format(pincount=pincount)

    # SMT type shrouded header,
    footprint_name = configuration['fp_name_format_string'].format(series=series, mpn=jst_name, num_rows=number_of_rows,
        pins_per_row=pincount, pitch=pad_spacing, orientation=orientation)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST GH series connector, {:s}, top entry type, ({:s})".format(jst_name, datasheet))
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags('connector jst GH SMT top vertical entry 1.25mm pitch')

    #create outline
    # create Courtyard
    # output kicad model

    #create pads
    #create pads
    createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_size, pad_y)

    #add mounting pads (no number)

    kicad_mod.append(Pad(number='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        at={'x':mpad_x, 'y':mpad_y}, size=mounting_pad_size, layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(number='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        at={'x':-mpad_x, 'y':mpad_y}, size=mounting_pad_size, layers=Pad.LAYERS_SMT))

    T = 0.5

    #add bottom line
    bottom_line_x = mpad_x + mounting_pad_size[0]/2 + pad_edge_silk_center_offset
    kicad_mod.append(Line(start=[bottom_line_x, oyt - configuration['silk_fab_offset']],
                            end = [-bottom_line_x, oyt - configuration['silk_fab_offset']],
                            layer='F.SilkS', width=configuration['silk_line_width']))

    #add top left corner (including pin 1 marker)
    kicad_mod.append(PolygoneLine(polygone=[{'x':-b_size_x/2 - configuration['silk_fab_offset'],'y': mpad_y + mounting_pad_size[1]/2 + pad_edge_silk_center_offset},
                                {'x':-b_size_x/2 - configuration['silk_fab_offset'],'y':oyb + configuration['silk_fab_offset']},
                                {'x':-A/2 - pad_size[0]/2 - pad_edge_silk_center_offset,'y':oyb + configuration['silk_fab_offset']},
                                {'x':-A/2 - pad_size[0]/2 - pad_edge_silk_center_offset,'y':pad_y +pad_size[1]/2}],
                                layer='F.SilkS', width=configuration['silk_line_width']))

    #add top right corner
    kicad_mod.append(PolygoneLine(polygone=[{'x':b_size_x/2 + configuration['silk_fab_offset'],'y':mpad_y + mounting_pad_size[1]/2 + pad_edge_silk_center_offset},
                                {'x':b_size_x/2 + configuration['silk_fab_offset'],'y': oyb + configuration['silk_fab_offset']},
                                {'x':A/2 + pad_size[0]/2 + pad_edge_silk_center_offset,'y': oyb + configuration['silk_fab_offset']}],
                                layer='F.SilkS', width=configuration['silk_line_width']))

    #add designator for pin #1
    kicad_mod.append(PolygoneLine(polygone=[{'x': -A/2 - 0.5,'y': oyb},
                               {'x': -A/2,'y': oyb - 1/sqrt(2)},
                               {'x': -A/2 + 0.5,'y': oyb}],
                                layer='F.Fab', width=configuration['fab_line_width']))



    #add fabrication layer details


    kicad_mod.append(RectLine(start={'x':oxl,'y':oyt}, end={'x':oxr,'y':oyb},
        layer='F.Fab', width=configuration['fab_line_width']))

    for i in range(pincount):
        x = -A/2 + (i * pad_spacing)
        y = oyb - 2
        s = 0.25

        kicad_mod.append(RectLine(start={'x':x-s,'y':y-s}, end={'x':x+s,'y':y+s},
            layer='F.Fab', width=configuration['fab_line_width']))


    #courtyard corners
    cx1 = mpad_x - mounting_pad_size[0]/2 - configuration['courtyard_distance']
    cx2 = -mpad_x + mounting_pad_size[0]/2 + configuration['courtyard_distance']

    cy1 = mpad_y - mounting_pad_size[1]/2 - configuration['courtyard_distance']
    cy2 = pad_y + pad_size[1]/2 + configuration['courtyard_distance']

    #add courtyard
    cx1 = roundToBase(cx1,configuration['courtyard_grid'])
    cx2 = roundToBase(cx2,configuration['courtyard_grid'])

    cy1 = roundToBase(cy1,configuration['courtyard_grid'])
    cy2 = roundToBase(cy2,configuration['courtyard_grid'])

    kicad_mod.append(RectLine(start={'x':cx1,'y':cy1}, end={'x':cx2,'y':cy2},
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    center = [0,-1.4]

    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **getTextFieldDetails(reference_fields[0], cy1, cy2, center)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **getTextFieldDetails(additional_ref, cy1, cy2, center)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=footprint_name,
        **getTextFieldDetails(value_fields[0], cy1, cy2, center)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **getTextFieldDetails(additional_value, cy1, cy2, center)))

    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}')

    lib_name = configuration['lib_name_format_string'].format(series=series)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv3.0.yaml')
    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for pincount in range(2,16):
        generate_one_footprint(pincount, configuration)
