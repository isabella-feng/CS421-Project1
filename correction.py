

# function to generate fixations at each word
def generate_fixations_left_skip_regression(aois_with_tokens):
    
    fixations = []
    word_count = 0
    skip_count = 0
    regress_count = 0
    
    aoi_list = aois_with_tokens.values.tolist()
    
    index = 0
    
    while index < len(aoi_list):
        x, y, width, height, token = aoi_list[index][2], aoi_list[index][3], aoi_list[index][4], aoi_list[index][5], aoi_list[index][7]
        
        word_count += 1
        
        fixation_x = x + width / 3 + random.randint(-10, 10)
        fixation_y = y + height / 2 + random.randint(-10, 10)

        last_skipped = False

        # skipping
        if len(token) < 5 and random.random() < 0.3:
            skip_count += 1 # fixations.append([fixation_x, fixation_y])
            last_skipped = True
        else:
            fixations.append([fixation_x, fixation_y, len(token) * 50])
            last_skipped = False
        
        # regressions    
        if  random.random() > 0.96:
            index -= random.randint(1, 10)

            if index < 0:
                index = 0

            regress_count += 1
        
        index += 1
            
    
    skip_probability = skip_count / word_count
    
    return fixations


# write a function generate offset error as described in the paper
def error_offset(x_offset, y_offset, fixations):
    '''creates error to move fixations (shift in dissertation)'''
    
    pass


# noise
import random

def error_noise(y_noise_probability, y_noise, duration_noise, fixations):
    '''creates a random error moving a percentage of fixations '''
    
    results = []
    
    for fix in fixations:

        x, y, duration = fix[0], fix[1], fix[2]

        # should be 0.1 for %10
        duration_error = int(duration * duration_noise)

        duration += random.randint(-duration_error, duration_error)

        if duration < 0:
            duration *= -1
        
        if random.random() < y_noise_probability:
            results.append([x, y + random.randint(-y_noise, y_noise), duration])
        else:
            results.append([x, y, fix[2]])
    
    return results

# slope
def error_slope(error_magnitude, fixations):
    '''creates an error moving a percentage of fixations '''

    '''Parameters:
    error_magnitude: range[0, 10], represent d_slope. error_magnitude == 0 -> d_slope == -0.1, upward sloping; error_magnitude == 10 -> d_slope == 0.1, downward sloping
    fixations: fixations data
    '''
    
    results = []
    d_slope = (-0.1) + (error_magnitude*0.02)

    for fix in fixations:
        x, y = fix[0], fix[1]
        results.append([x, y + (x*d_slope), fix[2]])
    
    return results

#shift
def error_shift(error_magnitude, fixations):
    '''creates an error moving a percentage of fixations '''

    '''Parameters:
    error_magnitude: range[0, 10], represent d_shift. error_magnitude == 0 -> d_shift == -1, upward shifting; error_magnitude == 10 -> d_shift == 1, downward shifting
    fixations: fixations data
    '''
    
    results = []
    d_slope = (-1) + (error_magnitude*0.2)

    for fix in range(len(fixations)):

        x, y = fixations[fix][0], fixations[fix][1]

        if fix == 0:
            results.append([x, y, fixations[fix][2]])
        else:
            results.append([x, y + (fix * d_slope), fixations[fix][2]])
    
    return results

#within-line regression
def error_within_line_reg(error_probability, fixations):
    '''creates an error moving a percentage of fixations '''

    '''Parameters:
    error_probability: probablity that formalizes the extent to which the reader performs within-line regressions
    fixations: fixations data
    '''
    
    results = []
    adjusted_prob = error_probability*0.1*0.5
    start_x = fixations[0][0]
    
    for fix in range(len(fixations)):

        x, y = fixations[fix][0], fixations[fix][1]

        if (fix > 0):
            if (random.random() < adjusted_prob) and (x > fixations[fix-1][0]):
                results.append([x - random.triangular(0, x-start_x, 0), y, fixations[fix][2]])
            else:
                results.append([x, y, fixations[fix][2]])
        else:
            results.append([x, y, fixations[fix][2]])
    
    return results

#between-line regression
def error_between_line_reg(error_probability, fixations, aois):
    '''creates an error moving a percentage of fixations '''

    '''Parameters:
    error_probability: probablity that formalizes the extent to which the reader performs within-line regressions
    fixations: fixations data
    '''

    line_coordinates = find_lines_Y(aois)
    fixes_in_lines = [[] for _ in range(len(line_coordinates))]

    for fix in fixations:
        y = fix[1]

        line = 0
        diff_y = abs(y - line_coordinates[0])

        for y_coor in line_coordinates:
            if abs(y - y_coor) < diff_y:
                diff_y = abs(y - y_coor)
                line = line_coordinates.index(y_coor)

        fixes_in_lines[line].append(fix)


    results = []
    adjusted_prob = error_probability*0.1

    #algorithm: if in probability, regress to the previous line and finish the previous line. Then finish the original line. Maximum one regression per line.
    for line_num in range(len(fixes_in_lines)):
        regressed = False

        if line_num == 0:
            for fix in fixes_in_lines[line_num]:
                results.append(fix)
        else:
            for fix_num in range(len(fixes_in_lines[line_num])):
                if fix_num == 0:
                    results.append(fixes_in_lines[line_num][fix_num])
                else:
                    if regressed:
                        results.append(fixes_in_lines[line_num][fix_num])
                    else:
                        if random.random() < adjusted_prob:
                            regress_line = int(random.triangular(0, line_num, line_num))
                            if fix_num >= (len(fixes_in_lines[regress_line])-1):
                                begin_fix = len(fixes_in_lines[regress_line])-1
                                results.append(fixes_in_lines[regress_line][begin_fix])
                            else:
                                begin_fix = fix_num
                                end_fix = random.randint(fix_num, len(fixes_in_lines[regress_line]))
                                for fix_num_prev in range(begin_fix, end_fix):
                                    results.append(fixes_in_lines[regress_line][fix_num_prev])
                            regressed = True
                        else: 
                            results.append(fixes_in_lines[line_num][fix_num])
    
    return results


from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
import numpy as np


def draw_fixation(Image_file, fixations):
    """Private method that draws the fixation, also allow user to draw eye movement order

    Parameters
    ----------
    draw : PIL.ImageDraw.Draw
        a Draw object imposed on the image

    draw_number : bool
        whether user wants to draw the eye movement number
    """

    im = Image.open(Image_file)
    draw = ImageDraw.Draw(im, 'RGBA')

    if len(fixations[0]) == 3:
        x0, y0, duration = fixations[0]
    else:
        x0, y0 = fixations[0]

    for fixation in fixations:
        
        if len(fixations[0]) == 3:
            duration = fixation[2]
            if 5 * (duration / 100) < 5:
                r = 3
            else:
                r = 5 * (duration / 100)
        else:
            r = 8
        x = fixation[0]
        y = fixation[1]

        bound = (x - r, y - r, x + r, y + r)
        outline_color = (50, 255, 0, 0)
        fill_color = (50, 255, 0, 220)
        draw.ellipse(bound, fill=fill_color, outline=outline_color)

        bound = (x0, y0, x, y)
        line_color = (255, 155, 0, 155)
        penwidth = 2
        draw.line(bound, fill=line_color, width=5)

        x0, y0 = x, y

    plt.figure(figsize=(17, 15))
    plt.imshow(np.asarray(im), interpolation='nearest')


def draw_correction(Image_file, fixations, match_list):
    """Private method that draws the fixation, also allow user to draw eye movement order

    Parameters
    ----------
    draw : PIL.ImageDraw.Draw
        a Draw object imposed on the image

    draw_number : bool
        whether user wants to draw the eye movement number
    """

    im = Image.open(Image_file)
    draw = ImageDraw.Draw(im, 'RGBA')

    if len(fixations[0]) == 3:
        x0, y0, duration = fixations[0]
    else:
        x0, y0 = fixations[0]

    for index, fixation in enumerate(fixations):

        if index < len(match_list):
        
            if len(fixations[0]) == 3:
                duration = fixation[2]
                if 5 * (duration / 100) < 5:
                    r = 3
                else:
                     r = 5 * (duration / 100)
            else:
                r = 8

            x = fixation[0]
            y = fixation[1]

            bound = (x - r, y - r, x + r, y + r)
            outline_color = (50, 255, 0, 0)
            
            if match_list[index] == 1:
            	fill_color = (50, 255, 0, 220)
            else:
            	fill_color = (255, 55, 0, 220)

            draw.ellipse(bound, fill=fill_color, outline=outline_color)

            bound = (x0, y0, x, y)
            line_color = (255, 155, 0, 155)
            penwidth = 2
            draw.line(bound, fill=line_color, width=5)

            # text_bound = (x + random.randint(-10, 10), y + random.randint(-10, 10))
            # text_color = (0, 0, 0, 225)
            # font = ImageFont.truetype("arial.ttf", 20)
            # draw.text(text_bound, str(index), fill=text_color,font=font)

            x0, y0 = x, y

    plt.figure(figsize=(17, 15))
    plt.imshow(np.asarray(im), interpolation='nearest')


def find_lines_Y(aois):
    ''' returns a list of line Ys '''
    
    results = []
    
    for index, row in aois.iterrows():
        y, height = row['y'], row['height']
        
        if y + height / 2 not in results:
            results.append(y + height / 2)
            
    return results



def find_word_centers(aois):
    ''' returns a list of word centers '''
    
    results = []
    
    for index, row in aois.iterrows():
        x, y, height, width = row['x'], row['y'], row['height'], row['width']
        
        center = [int(x + width // 2), int(y + height // 2)]
        
        if center not in results:
            results.append(center)
            
    return results


def find_word_centers_and_duration(aois):
    ''' returns a list of word centers '''
    
    results = []
    
    for index, row in aois.iterrows():
        x, y, height, width, token = row['x'], row['y'], row['height'], row['width'], row['token']
        
        center = [int(x + width // 2), int(y + height // 2), len(token) * 50]

        if center not in results:
            results.append(center)
    
    #print(results)
    return results



def overlap(fix, AOI):
    """checks if fixation is within AOI"""
    
    box_x = AOI.x
    box_y = AOI.y
    box_w = AOI.width
    box_h = AOI.height

    if fix[0] >= box_x and fix[0] <= box_x + box_w \
    and fix[1] >= box_y and fix[1] <= box_y + box_h:
        return True
    
    else:
        
        return False
    
    
def correction_quality(aois, original_fixations, corrected_fixations):
    
    match = 0
    total_fixations = len(original_fixations)
    results = [0] * total_fixations
    
    for index, fix in enumerate(original_fixations):
        
        for _, row  in aois.iterrows():
            
            if index < len(corrected_fixations):
                if overlap(fix, row) and overlap(corrected_fixations[index], row):
                    match += 1
                    results[index] = 1
                
    return match / total_fixations, results