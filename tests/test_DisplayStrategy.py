import pytest
import random
from libs.Helpers.GeneralHelpers import *
from libs.DisplayStrategies.AdvancedDisplayStrategy import *
from libs.DisplayStrategies.MessageViewer import *
from libs.CtypesLibs.CPPFrameToString import FrameToString


HOST = '10.0.0.147'
PORT = 9001

@pytest.fixture
def advanced_display_strategy():
    display_strategy = AdvancedDisplayStrategy(host=HOST, port=PORT, scale_percentage=100)
    return display_strategy

@pytest.fixture
def frame_to_string():
    frame_to_string = FrameToString()
    return frame_to_string

def test_update_canvas_1(advanced_display_strategy: AdvancedDisplayStrategy):
    delim_a = chr(1) # end of color
    delim_b = chr(2) # end of row

    message = ""

    # row 0
    message += chr(0 + OFFSET)
    # color 0
    message += rgb_to_utf8(r=12, g=5, b=50, offset=OFFSET)

    # range 0 column start
    message += chr(3 + OFFSET)
    # range 0 span
    message += chr(2 + OFFSET)

    # range 1 column start
    message += chr(13 + OFFSET)
    # range 1 span
    message += chr(4 + OFFSET)

    # delim a <?>
    message += delim_a

    # Done applying color 0 to this row. Are there any other colors?
    # yes.
    # color 1
    message += rgb_to_utf8(r=120, g=50, b=250, offset=OFFSET)
    # range 0 column start
    message += chr(23 + OFFSET)
    # range 0 span
    message += chr(5 + OFFSET)

    # range 1 column start
    message += chr(33 + OFFSET)
    # range 1 span
    message += chr(2 + OFFSET)

    message += delim_a
    # Done applying color 0 to this row. Are there any other colors?
    # no
    message += delim_b

    update_canvas(message=message, canvas=advanced_display_strategy.canvas, offset=OFFSET)
    advanced_display_strategy.display()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def test_update_canvas_2(advanced_display_strategy: AdvancedDisplayStrategy):
    FRAME_WIDTH = DEFAULT_FRAME_WIDTH
    FRAME_HEIGHT = DEFAULT_FRAME_HEIGHT

    delim_a = chr(1)  # end of color
    delim_b = chr(2)  # end of row
    message = ""

    data = {}

    for row in range(FRAME_HEIGHT):
        # Append row
        message += chr(row + OFFSET)

        # Randomly select the number of colors for this row
        num_colors = random.randint(1, 3)
        data[row] = num_colors

        for _ in range(num_colors):
            # Randomly select RGB values
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            # Append color
            message += rgb_to_utf8(r, g, b, offset=OFFSET)

            # Randomly select the number of color ranges for this color
            num_ranges = random.randint(1, 3)

            for _ in range(num_ranges):
                # Randomly select start of color range
                start = random.randint(0, FRAME_WIDTH - 2)

                # Randomly select range span. It must not exceed the amount of columns from the start
                span = random.randint(1, FRAME_WIDTH - start - 1)

                # Append range start and span
                message += chr(start + OFFSET)
                message += chr(span + OFFSET)

            # Append end of color delimiter
            message += delim_a

        # Append end of row delimiter
        message += delim_b

    # Update and display canvas
    advanced_display_strategy.update_canvas(message=message)
    advanced_display_strategy.display()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return



def test_update_canvas_from_cpp(frame_to_string: FrameToString, advanced_display_strategy: AdvancedDisplayStrategy):
    # Initialize the arrays to be all the same color, say, bright red.
    last_state = np.full((350, 350, 3), [0, 0, 0], dtype=np.uint8)  # Initialize last_state with black color

    current_state = np.copy(last_state)  # Create a copy of last_state as current_state

    # Modify specific regions in current_state

    current_state[10:50, 100:150] = [94, 13, 73]  # Change row 10 to 49 and column 100 to 149.
    current_state[100:150, 50:100] = [23, 37, 201]  # Change row 100 to 149 and column 50 to 99.
    current_state[200:250, 150:200] = [19, 120, 9]  # Change row 200 to 249 and column 150 to 199.
    current_state[125:175, 200:250] = [190, 37, 59]  # Change row 200 to 249 and column 200 to 249.
    current_state[0:50, 0:50] = [75, 150, 30]  # Change row 0 to 49 and column 0 to 49.

    # Since the last state, we added colors, which are in the current state.

    cv2.imshow("current_state", current_state)
    current_state_constructed_by_message = last_state

    message = frame_to_string.get_string(current_state, last_state)
    advanced_display_strategy.update_canvas(message=message,
                                            canvas=current_state_constructed_by_message)
    cv2.imshow("Current state constructed by message", current_state_constructed_by_message)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return




def test_update_canvas_from_hardcoded_message(frame_to_string: FrameToString, advanced_display_strategy: AdvancedDisplayStrategy):
    # Initialize the arrays to be all the same color, say, bright red.
    current_state_constructed_by_message = np.full((240, 256, 3), [0, 0, 0], dtype=np.uint8)  # Initialize last_state with black color
    # complete smb title screen
    message = """ 𐑪Đ㪩𐑪㺑𐠏巒煚蓣鱖뽾𣪒𤸚𥶽𧤖𩰺𫞕𱤾𳡾𵏒𶝚𷌗𐑪(斣礫邛돃훪朗𤉣𥗪𧅂𩂃𪐍𬬬𳂪𴿩𵮣𶼩𸺁䉹𐠏巓浳胺貲鱒꿚읊𣪒𤸚𥧒𦵚𧤒𨲚𩰺𫞒𬜲𲄊𴁊𵏓𶍳𷌒𐑪(榉礪裉钂ꐣ랬켛ﹹ𤉣𥗩𦆣𧔩𨃣𩑪𪐍𫽢𬼕𲣞𴠛𵾉𶼩𷫾䙡𐠏巗紒邚鱒꿚읊𣪒𤙉𤸚𥧒𦵚𧤒𨲚𩰺𫞒𬬚𲄊𴁊𵏗𷌒𐑪(礩蓣顩ꐣ랬켛ﹹ𤉡𤨱𥗩𦆣𧔩𨃣𩑪𪐍𫽣𭋼𲣞𴠛𶼩𷫾䩉𐠏巗紒邚鱒꯳읊𣪗𥧒𦵚𧤒𨢳𩰺𫞒𬬚𲄊𴁊𵏗𷌖𐑪(礩蓣顩ꐢ랬켛ﹹ𥗩𦆣𧔩𨃢𩑪𪐍𫽣𭋼𲣞𴠛𶼩𸪚丱𐠏巒榉煚紗鱕읊𣪗𥧒𦵚𧤕𩰺𫞒𬬚𲄊𴁊𵏒𵾉𶝚𷌒𐑪(斡浱礩顩꿞켛ﹹ𥗩𦆣𧔩𨲜𪐍𫽣𭋼𲣞𴠛𵮡𶍱𶼩𷫾则𐠏巒煚紒邚鱒ꠋ읊𣪓𤨳𥧒𦵚𧤒𨓋𩰺𫞒𬜲𲄊𴁊𵏒𶝚𷌒𐑪(斣礩蓣顩ꐡ독켛ﹹ𤙉𥗩𦆣𧔩𨃡𩂃𪐍𫽢𬼕𲣞𴠛𵮣𶼩𷫾嘁𐠏巒煚紒邚鱒꯳뽾𣪒𤸚𥶽𧤒𨢳𩰾𫞕𲄊𳡾𵏒𶝚𷌗𐑪(斣礩蓣顩ꐢ랪훪朗𤉣𥗪𧅂𨃢𩑪𫎩𬬮𲣜𴿩𵮣𶼩𸺁姩𐑪Đ巑𖽱䕏𖞢𐠏斣蓣ꐣ썣𐧣𚘣𜕣𦖊𪐊𐑪*煝邝꿝켝𑖭𗍥𛇝𝄾𦵦𪰫憹𗍙䕏𖎼𐠏憹浲胹貲ꀹ꯲뽹쬲𐗹𑆲𚈹𚷲𜅹𜴲𦆣𪀣𐑪)斢畃蓢钃ꐢ돃썢팃暑𐧢𑦓𗝋𚘢𛗃𜕢𝔤𦵥𪰫斡𗍙䕏𖎼𐠏巒煚紒邚鱒꿚뮒켚𐈒𑖚𘋹𙊙𙹒𛇚𛶒𝄚𦖊𪐊𐑪(斣礩蓣顩ꐣ랩썣훩︩𐧣𑵺𗝃𘛣𙚂𚘣𛦩𜕣𝤌𦵦𪰫榉𗍙䕏𖎼𐠏巒煚紒邚鱒꿚뮒켚𐈒𑖚𘛡𘺱𙹒𛇚𛶒𝄚𦖊𧳾𪐊𐑪(斣礩蓣顩ꐣ랩썣훩︩𐧣𑵺𗝄𘫉𙊛𚘣𛦩𜕣𝤌𦵜𩑬𪰫浱𗍙䕏𖎼𐠏巒煚紒邚鱒꿚뮒켚𐈒𑖚𘫉𙹒𛇚𛶒𝄚𦖊𧳾𪐊𐑪(斣礩蓣顩ꐣ랩썣훩︩𐧣𑵺𗝅𘺴𚘣𛦩𜕣𝤌𦵜𩑬𪰫煙𗍙䕏𖎼𐠏憺煙胺邙ꀺ꿙뽺켙𐗺𑖙𘛡𘺱𚈺𛇙𜅺𝄙𦖊𪐊𐑪)榊畃裊钃ꠊ돃읊팃暑𐷊𑦓𗝄𘫉𙊜𚨊𛗃𜥊𝔥𦵦𪰫畁ጉ𗍙䕏𖞢𖎹𖽱𐠏斣蓣ꐣ썣𐧣𘋹𙊙𚘣𜕣𥶾𩰾𐑪*煝邝꿝켝𑖬𗝃𘛣𙚄𛇝𝄼𧔲𫏹礩ጉ𖽱𖞢𐑪j𗏻紑뛌ꃦ𐑪9𵀑胺𴿩ጉꃦ뛌鱑𐑪8𵏸蓡𐑪裉𴿩ጉꀺ끾𴠚뛌鱑ꠊ𴁊𐑪8𵏸貱꿙𴠙𴿩ጉꀺ둥𴰁뛌鱑ꠊ𴁊𐑪8𵏸邙꯲𴐲𴿩ጉꀻ둦𴰁뛌鱑𐑪8𵏸钂𴿩ጉꃦ뛌鱑𐑪8𵏸顩𐑪鱑𴿩ጉꁃ𑵪𓲪𖽸𛦪𞳋뛌鱑쬸𐗾𒔾𔒃𘺻𜆃𐑪8𵏸ꀺ𴿩ጉꁂ𑵪𓲪𗍞𛦪🂲뛌鱑읒𐗾𒔾𔒄𘫔𜆄𐑪8𵏸ꐡ𐑪ꠉ𴿩ጉꁁ暑𑵪𓲪𗝄𛦪💙뛌鱑썬𐗾𒔾𔒅𘛭𜆅𐑪8𵏸꯱𑵩𓲩𛦩𴿩ጉꁁ暑𒅑𔂑𗝄𛶑💙뛌鱑썬𐗾𒔾𔒅𘛭𜆅𐑪8𵏸꿛𑵩𓲩𛦩𴿩ጉꁀ︪𒅑𔂑𗬪𛶑🢀뛌鱑뾆𐗾𒔾𔒆𘌆𜆆𐑪8𵏸랩𐑪뮑𑵩𓲩𕯩𗬩𙩱𝣩🠩𴿩ጉꁀ︪𒅑𔂑𗼑𛶑🱧뛌鱑뽿𐗾𒔾𔑾𕿗𘋾𜅾𝳗𐑪8𵏸뽹𑵩𓲩𕯩𗬩𙩩𛗂𝣩🠩𴿩ጉꁀ𐈑𒅑𔂑𗼑𛶑🱧뛌鱑뾀𐗾𒔾𔑾𕿗𘋾𙹖𜅾𝳗𐑪8𵏸썡𑵩𓲩𕯩𗬩𙩩𛗂𝣩🠩𴿩ጉꁁ𐈑𒅑𔂑𗼑𛶑🱧뛌鱑썩𐗾𒔾𔑾𕿗𘋾𙹖𜅾𝳗𐑪8𵏸읉𑵩𓲩𕯩𗝂𙩩𛗂𝣩👂𴿩ጉꁁ𐈑𒅑𔂑𗼑𛶑🱧뛌鱑썫𐗾𒔾𔑾𕿖𘋾𙹖𜅾𝳖𐑪8𵏸쬱썡𑵩𓲩𕯩𗝂𙩩𝣩🁛𴿩ጉꁁ暑𒅑𔂑𗼑𛗃🱧뛌鱑읓𐗾𒔾𔑾𕿖𘋾𙹖𜅾𝳕𐑪8𵏸켙썣𑵩𓲩𕯩𗍛𙩩𛗁𝣩👂𴿩ጉꁁ暑𒅑𔂑𗼑𛦪🱧뛌鱑켡𐗾𒔾𔑾𕿕𘋾𙹖𜅾𝳖𐑪8𵏸팁음𑵩𓲩𕯩𗍛𙩩𛗁𝣩🠩𴿩ጉꁂ︪𒅑𔂑𗼑𛦪🱧뛌鱑훰𐗾𒔾𔑾𕿕𘋾𙹖𜅾𝳗𐑪8𵏸훩읎𑵩𓲩𕯩𖽳𙩩𚈾𝣩𴿩ጉꁂ︪𒅑𔂑𗬪𙹑𛦪🢀뛌鱑𐗾𒔾𔑾𕿔𘋾𜅾𝳗𐑪8𵏸𓲩𕯩𖎾𝣩𴿩ጉꁀ︪𔂑𕿑𗬪𛦪𝳑🢀뛌鱑뾆𐘆𔑾𘌆𜅾𞂾𐑪8𵏸𓲩𕯩𖎽𝣩𴿩ጉꁀ︪𔂑𕿑𗝃𛦪𝳑🢀뛌鱑뾆𐘆𔑾𘌆𜅾𞂾𐑪8𵏸︩𓲩𕯩𖎽𝣩🠩𴿩ጉꁀ𐈑𔂑𕿑𗝃𛦪𝳑🱧뛌鱑뾆𐘆𔑾𘌆𜅾𞂾𐑪8𵏸既𓣂𕯩𖎼𝣩🠩𴿩ጉꁁ𐈒𔂑𕿑𗍝𛦪𝳑🱧뛌鱑썬𐧬𔑾𘛭𜅾𞂾𐑪8𵏸既𓣂𕯩𛦩𝣩🠩𴿩ጉꁁ𐈒𔂑𕿚𛶑𝳑🱧뛌鱑썬𐧬𔑾𘛭𜅾𞂾𐑪8𵏸썡𐧡𓓛𕯩𘛡𛦩𝣩🠩𴿩ጉꁁ𐈒𔂑𕿚𛶑𝳑🱧뛌鱑읒𐷒𔑾𘫔𜅾𞂾𐑪8𵏸敏𐑪︩읉𐷉𓃳𕯩𘫉𛦩𝣩🠩𴿩ጉꁂ︬𓲪𕿛𛶑𝳑🱧뛌鱑쬸𑆸𔑾𘺻𜅾𞂾𐑪8𵏸𐈑읔𐷔𔡦𘫕𜕦𞒦𴿩ጉꁂ︬𓲫𕿛𛶒𝳒🱧뛌鱑𐑪8𵏸𐗺쬺𑆺𔡦𘺼𜕦𞒦𴿩ጉꁃ渚𓣄𕿜𛶒𝳒🱧뛌鱑𐑪8𵏸𐧡𐑪𐷉켠𑖠𔡦𙊣𜕦𞒦𴿩ጉꁄ𓓝𕿝𛶒𝳒🱧뛌鱑𐑪8𵏸𑆴𴿩ጉꃦ뛌鱑𐑪8𵏸𑵩𐑪𒅑𴿩ጉꁃ𑆸𕀵𘺵𛦭𞱽𤨵𨢸𬜸𰗃뛌鱑쬵︭𓃸𖏃𚈾𜴸𡽃𥷃𪟸𮙸𐑪8𵏸𒔺𴿩ጉꁂ𑖞𕐜𙊜𛦬🁤𤸜𨲞𬬞𰦪뛌鱑읏漢𒴒𖏄𚈾𜥒𡽄𥷄𪐒𮊒𐑪8𵏸𒤡𐑪𒴉𴿩ጉꁁ𑦄𕠃𙚃𛦫👋𥈃𩂄𬼄𰶑뛌鱑썩𒤬𖏅𚈾𜕬𡽅𥷅𪀬𭺬𐑪8𵏸𓃱𛦩𴿩ጉꁁ𑦄𕠃𙚃𛶒👋𥈃𩂄𬼄𰶑뛌鱑썩𒤬𖏅𚈾𜕬𡽅𥷅𪀬𭺬𐑪8𵏸𓓛𛦩𴿩ጉꁀ𑵪𕯪𙩪𛶑🠲𥗪𩑪𭋪𱅸뛌鱑뾎𒕆𖏆𚈾𜆆𡽆𥷆𩱆𭫆𐑪8𵏸𓲩𐑪𔂔훪︪𑵩𓲪𕯩𗬪𙩩𛦩𝣪🠩𣚪𥗩𧔪𩑩𫎪𭋩𯈪𱅩𴿩ጉꁀ𒅑𕿑𙹑𛶑🰙𥧑𩡑𭛑𱕟뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜅾𞂾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𐑪8𵏸𔱉𐑪𕀴훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𣚩𥗩𧔩𩑩𫎩𭋩𯈩𱅩𴿩ጉꁀ𐈑𒅑𔂑𕿑𗼑𙹑𛶑𝳑🰙𣪑𥧑𧤑𩡑𫞑𭛑𯘑𱕟뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜅾𞂾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𐑪8𵏸𕯩𐑪𕿑훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𣚩𥗩𧔩𩑩𫎩𭋩𯷦𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛑𯘒𱕟뛌鱑뽾𐗾𒔾𔑾𖎾𗼗𚈾𜅾𞂾𡼾𣪗𥶾𧤗𩰾𫭾𭪿𐑪8𵏸𖎹훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𣚩𥗩𧔩𩑩𫎩𭋩𯷦𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛑䩶𱕟뛌鱑뽾𐗾𒔾𔑾𖎾𗼗𚈾𜅾𞂾𡼾𣪗𥶾𧤗𩰾𫭾𭫀𐑪8𵏸𖞡훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𣚩𥗩𧔩𩑩𫎩𭋩𰇍𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛒𱕟뛌鱑뽾𐗾𒔾𔑾𖎾𗼗𚈾𜅾𞂾𡼾𣪗𥶾𧤗𩰾𫭾𭺩𐑪8𵏸𖮉훩︩𑵩𓲩𕯩𗬩𙚂𛦩𝣩🠩𣚩𥈂𧔩𩂂𫎩𭋩𰦛𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛒𱕟뛌鱑뽾𐗾𒔾𔑾𖎾𗼖𚈾𜅾𞂾𡼾𣪖𥶾𧤖𩰾𫭾𭺫𐑪8𵏸𖽱훩︩𑵩𓲩𕯩𗬩𙊛𛦩𝣩🠩𣚩𤸛𧔩𨲛𫎩𭋩𭺡𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛒𰶑뛌鱑뽾𐗾𒔾𔑾𖎾𗼕𚈾𜅾𞂾𡼾𣪕𥶾𧤕𩰾𫭾𮊓𐑪8𵏸𗍙훩︩𑵩𓲩𕯩𗬩𙚂𛦩𝣩🠩𣚩𥈂𧔩𩂂𫎩𭋩𭺣𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛒𰶑뛌鱑뽾𐗾𒔾𔑾𖎾𗼖𚈾𜅾𞂾𡼾𣪖𥶾𧤖𩰾𫭾𮩡𐑪8𵏸𗝁훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𣚩𥗩𧔩𩑩𫎩𭋩𮊌𴿩ጉꁀ𐈑𒅑𔂑𕿑𙹑𛶑𝳑🰙𥧑𩡑𫞑𭛓𱅸뛌鱑뽾𐗾𒔾𔑾𖎾𗼗𚈾𜅾𞂾𡼾𣪗𥶾𧤗𩰾𫭾𯈰𐑪8𵏸𗬩훩︩𑵩𓲩𕯩𗬩𛦩𝣩🠩𣚩𧔩𫎩𭋩𮊎𴿩ጉꁀ𐈑𒅑𔂑𕿑𙩪𛶑𝳑🰙𥗪𩑪𫞑𭛓𱅸뛌鱑뽾𐗾𒔾𔑾𖎾𗼗𚈾𜅾𞂾𡼾𣪗𥶾𧤗𩰾𫭾頋𐑪8𵏸𗼒훩︩𑵩𕯩𗬩𛦩𝣩🠩𣚪𧔩𫎩𭋩𯈪𴿩ጉꁀ𐈑𒅑𕿑𗼑𙩪𛶑𝳑🰙𥗪𧤑𩑪𫞑𭛑𱅸뛌鱑뽾𐗾𒕆𖎾𘋾𚈾𜅾𞂾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𐑪8𵏸𘋹𐑪𘛢훩︩𑵩𕯩𗬩𙩩𛦩𝣩🠩𣚪𥗩𧔩𩑩𫎩𭋩𯘑𱅩𴿩ጉꁀ𐈑𒅑𕿑𗼑𙹑𛶑𝳑🰙𥧑𧤑𩡑𫞑𭛑𯈩𱕟뛌鱑뽾𐗾𒕆𖎾𘋾𚈾𜅾𞂾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𐑪8𵏸𘫉𐑪𘺴훩︩𑵩𕯩𗬩𙩩𛦩𝣩🠩𣚩𥗩𧔩𩑩𫎩𭋩𯈩𱅩𴿩ጉꁀ𐈑𒅑𕿑𗼑𙹑𛶑𝳑🰙𣪑𥧑𧤑𩡑𫞑𭛑𯘑𱕟뛌鱑뽾𐗾𒕆𖎾𘋾𚈾𜅾𞂾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𐑪8𵏸𙩩𐑪𙹓훩︩𑵩𓲪𕯩𗬩𙩩𛦩🠩𣚩𥗩𧔩𩑩𭋩𱅩𴿩ጉꁀ𐈑𒅑𕿑𗼑𙹑𛶑🰙𥧑𧤑𩡑𭛑𱕑𳂰뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜆆𡼾𣪗𥶾𧳾𩱆𭫆𱤾𐑪8𵏸𚘡𐑪𚨉훩︩𑵩𓲪𕯩𗬩𙩩𛦩👂𣚩𥈂𧔩𩑩𬼂𰶂𴿩ጉꁀ𐈑𒅑𕿑𗼑𙹑𛶒🰙𥧑𧤑𩡒𭛒𱕑𳂰뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜕬𡼾𣪖𥶾𧳾𪀬𭺬𱤾𐑪8𵏸𚷱훩︩𑵩𓲩𕯩𗬩𙩩𛦩👂𣚩𥈂𧔩𩑩𬼂𰶂𳂩𴿩ጉꁀ𐈑𒅑𔂑𕿑𗼑𙹑𛶒🰙𥧑𧤑𩡒𭛒𱕑𳒗뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜕬𡼾𣪖𥶾𧳾𪀬𭺬𱤾𐑪8𵏸𛇚훩︩𑵩𓲩𕯩𗬩𙩩𛦩𜕡🁛𣚩𤸛𧔩𩑩𪀡𬬛𭺡𰦛𳂩𴿩ጉꁀ𐈑𒅑𔂑𕿑𗼑𙹑𛶒🰙𥧑𧤑𩡒𭛒𱕑𳒗뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜥒𡼾𣪕𥶾𧳾𪐒𮊒𱤾𐑪8𵏸𛗁𐑪𛦩훩︩𑵩𓲩𕯩𗬩𙩩𛦩𜥉𞱳𣚩𤨳𧔩𩑩𪐉𬜳𮊉𰖳𳂩𴿩ጉꁀ𐈑𒅑𔂑𕿑𗼑𙹑𛶓🠲𥗪𧤑𩡓𭋬𱅪𳒗뛌鱑뽾𐗾𒔾𔑾𖎾𘋾𚈾𜴸𡼾𣪔𥶾𧳾𪟸𮙸𱤾𐑪8𵏸𛶑썦𐧦𒤦𔡦𖞦𘛦𚘦𜥔𢌦𣹾𦆦𨃦𪐔𮊔𱴦𴿩ጉꁁ𐈒𒅒𔂒𕿒𗼒𙹒𛶓🠳𣪑𥗫𧤒𩡓𭋬𱅫𳒗뛌鱑𐑪8𵏸𜅺썦𐧦𒤦𔡦𖞦𘛦𚘦𜴺𢌦𣹽𦆦𨃦𪟺𮙺𱴦𴿩ጉꁁ𐈒𒅒𔂒𕿒𗼒𙹒𛶔👌𣪑𥈄𧤒𩡔𬼆𰶄𳒗뛌鱑𐑪8𵏸𜕡𐑪𜥉썦𐧦𒤦𔡦𖞦𘛦𚘦𝄠𢌦𣹼𦆦𨃦𪯠𮩠𱴦𴿩ጉꀺ꿝𐈒𒅒𔂒𕿒𗼒𙹒𛶕🁥𣪑𤸝𧤒𩡕𬬠𰦝𳒓𴠚뛌鱑ꠊ𴁊𐑪8𵏸𜴱꿙𴠙𴿩ጉꀺ둥𴰁뛌鱑ꠊ𴁊𐑪8𵏸𝄙꯲𴐲𴿩ጉꀻ둦𴰁뛌鱑𐑪8𵏸𝔁𴿩ጉꃦ뛌鱑𐑪8𵏸𝣩ꃦ𐑪9𵀑𝳑뛌𚘤𜥊𞂽🿽𡭖𥧒𦵚𧳾𩡒𪯚𫭾𭛗𯘒𰦚𱕕𳡽𐑪z𛗅𝄜👃𡎂𣋊𦆣𧔪𩑩𪀣𫎪𭋩𯈩𯷣𱅩𲣜𴰪𞂹뛌𚈹𛗁𜕣𝳒🁚🰒𠾚𡭒𥧓𦵚𨓊𩡓𪯚𬍊𭛒𯘓𰦚𱕒𲓲𳒒𴠚𐑪y𚘤𛦫𝄛𞒣🠩𠏣𡝩𢌮𦖊𧔬𨲛𪐊𫎬𬬛𭺦𰇊𱅩𱴢𲳂𳱣𵀑𞒡뛌𙹑𚨊𛦩𜥊𝳒🁚🰒𠾚𡭖𥧔𦵚𨓊𩡔𪯚𬍊𭛒𯘔𰦚𱕒𲣚𳒒𴠚𐑪x𚈺𛇚𛶓𝄛𞒣🠩𠏣𡝩𣋊𦥱𧔬𨲛𪟱𫎬𬬛𭺦𰖱𱅩𱴣𳂩𳱣𵀑𞢉뛌𙹑𚘡𛦩𜥊𞂾🿽𢻚𥧗𨓊𩡗𬍊𭛖𯘗𱕒𲣚𳒒𴠚𐑪x𚈹𚨌𛶓𝄜🠪𡎇𣚱𧔬𨲛𫎬𬬛𮹂𱅩𱴣𳂩𳱣𵀑𞱱뛌𙹑𚘡𛦩𜥊🁚🰒𠾚𢻚𥧒𦖌𨓊𩡒𪐌𬍊𭛒𯘒𰇌𱕒𲣚𳒒𴠚𐑪x𚈹𚨌𛶓𝄠🠩𠏣𡝮𣚱𦆡𧔬𨲛𪀡𫎬𬬛𭺦𯷡𱅩𱴣𳂩𳱣𵀑🁙뛌𙹑𚨊𛦩𜥊𞱲🰒𠾚𡭒𢻚𥧒𦥳𨓊𩡒𪟳𬍊𭛒𯘒𰖳𱕒𲓲𳒒𴠚𐑪x𚈺𛇚𛶓𝄟👂𠏣𡝩𢌣𣚱𦆢𧔬𨲛𪀢𫎬𬬛𭺦𯷢𱅩𱴢𲳂𳱣𵀑👁뛌𚈹𛗁𜅾𞂼🿽𡼽𥧒𦵚𧳾𩡒𪯚𬍊𭛗𯘒𰦚𱕕𳡽𐑪y𚘤𛦪𝣪🁜𡎃𣋊𦆣𧔪𩑩𪀣𫎬𬬛𯈩𯷣𱅩𲣜𴰪🠩뛌𚘤𐑪z𛙒🰠𐑪Đ𣚩𐑪𣪑𐠏𖮊𙹖𜅺𞒣🿺𠾚𡭗𣪖𨃥𪀣𫞒𬬚𭛗ጉ𒤤𐑪Z𓣍𗍣𛗃𜥏🁜𠟊𡝩𣚩𥈌𩑫𪯛𫽣𭋩𯉩𣹹𐠏𖞣𙹒𛇚𜅺𞂺𞱲🿺𠾚𡭒𣪒𤸚𧳺𩰺𪟲𫞓𬜳𭛒ጉ𒔾𐑪Y𓲳𗍣𚘣𛦪𜥎𞢉👃𠟊𡝩𢌦𤉣𥗲𨓎𪐉𪿂𬍉𭋩𭻦𤉡𐠏𖮊𙹒𛇚𜅺𝳒🁚🿺𠾚𡭒𣪒𤸚𧤒𩡒𪯚𫞗𭛒ጉ𒔾𐑪Y𓲴𗍣𚘣𛦪𜥍𞒣🠪𠟊𡝩𢌦𤉣𥗱𨃦𪀣𫎩𭋩𭻦𤙉𐠏𖮊𙹒𛇚𜅺𝳒🁚𠏤𡭖𣪒𤨳𧤒𨢳𩡒𪯚𫞗𭛖ጉ𒅘𐑪X𔂛𗍣𚘣𛦪𜥍𞒣🠫𡎂𣋂𤉢𥗱𨃢𩑩𪀣𫎩𭋩𮺂𤨱𐠏𖮊𙹖𜅺𝳗𠟊𡭒𣪕𧤒𨲚𩡗𫞒𬍉𬬚𭛒ጉ𒅘𐑪X𔂛𗍣𛗃𜥍🠬𠾛𢌦𤸣𨃣𩑩𫎩𫽡𬜱𭋩𭻦𤸙𐠏𖮊𙹒𜅺𝳒🁚𠟊𡭒𣪒𤙋𧳺𨲚𩡒𪯚𫞒𬬚𭛒ጉ𒅘𐑪X𔂛𗍣𚘧𜥍𞒣🠬𠾛𢌦𤉡𥈋𨓊𩑩𪀣𫎩𫽣𭋩𭻦𥈁𐠏𖎾𙹒𜅾𝳒🁚𠟊𡭗𣪒𤨳𨃥𩡒𪯚𫞒𬬚𭛗뛌𒤤𒔹𓣁𐑪Y𓲲𗬱𚘧𝣩𞒣🠬𠾛𣚩𤉢𥗳𩑩𪀣𫎩𫽣𭋩𯉩𥗩뛌𒤤𐑪Z𓥲𥧘𐑪Đ𧔩𐑪𧤑𐠏𖎽𙹖𜅺𞒣🿺𠾚𡭗𣪖𨃥𪀣𫞒𬬚𭛗𐑪i𗝊𛗃𜥏🁜𠟊𡝩𣚩𥈌𩑫𪯛𫽣𭋩𯉩𧳹𐠏𕿒𗍚𙹒𛇚𜅺𞂺𞱲🿺𠾚𡭒𣪒𤸚𧳺𩰺𪟲𫞓𬜳𭛒𐑪h𖞣𗬱𚘣𛦪𜥎𞢉👃𠟊𡝩𢌦𤉣𥗲𨓎𪐉𪿂𬍉𭋩𭻦𨃡𐠏𖽳𙹒𛇚𜅺𝳒🁚🿺𠾚𡭒𣪒𤸚𧤒𩡒𪯚𫞗𭛒𐑪l𗬱𚘣𛦪𜥍𞒣🠪𠟊𡝩𢌦𤉣𥗱𨃦𪀣𫎩𭋩𭻦𨓉𐠏𖞤𙹒𛇚𜅺𝳒🁚𠏤𡭖𣪒𤨳𧤒𨢳𩡒𪯚𫞗𭛖𐑪j𗝊𚘣𛦪𜥍𞒣🠫𡎂𣋂𤉢𥗱𨃢𩑩𪀣𫎩𭋩𮺂𨢱𐠏𖎼𙹖𜅺𝳗𠟊𡭒𣪕𧤒𨲚𩡗𫞒𬍉𬬚𭛒𐑪i𗍣𛗃𜥍🠬𠾛𢌦𤸣𨃣𩑩𫎩𫽡𬜱𭋩𭻦𨲙𐠏𕿓𙹒𜅺𝳒🁚𠟊𡭒𣪒𤙋𧳺𨲚𩡒𪯚𫞒𬬚𭛒𐑪h𖮕𚘧𜥍𞒣🠬𠾛𢌦𤉡𥈋𨓊𩑩𪀣𫎩𫽣𭋩𭻦𩂁𐠏𕿗𙹒𜅾𝳒🁚𠟊𡭗𣪒𤨳𨃥𩡒𪯚𫞒𬬚𭛗𐑪h𗬱𚘧𝣩𞒣🠬𠾛𣚩𤉢𥗳𩑩𪀣𫎩𫽣𭋩𯉩𩑮𐑪Đ𪟱𐑪𪯙邞𐑪5꣝𪿁蓣ꠋՐ邞𐑪2뒒𫎩紒돂Ր蓬𐑪0뱠𫞑礩꿙뮑Ր紝돂𐑪/쁇𫭹畁꯳뽹Ր礵랪𐑪.쐮𫽡煙꯳썡Ր畎랫𐑪-정𬍉浱꯳읉Ր照랬𐑪,쯼𬜱榉ꀺ꯳쬱Ր浽ꠉ랭𐑪+쿣𬬙斡ꀺ꿙켙Ր榖ꠊ돇𐑪*폊𬼁憹ꀺ팁Ր斯ꠓ𐑪)ힱ𭋩巑ꀺ훩Ր懈ꠔ𐑪(𭛑𐠏𘋾𚈽𛶖𢌣𤉣𦆣𨃣𪀣𫽣姩Ր巰𐑪'𙩪𛗂𝔔𢻝𤸝𦵝𨲝𪯝𬭣𭪹𐠏𘫊𙹒𛇚𛶒𝄚𡼹𢫲𣹹𤨲𥶹𦥲𧳹𨢲𩰹𪟲𫭹𬜲嘁Ր娊𐑪&𙊛𚘣𛦩𜕣𝣺𢌢𣋃𤉢𥈃𦆢𧅃𨃢𩂃𪀢𪿃𫽢𬽊𭺡𐠏𘫊𙹒𛇚𛶒𝄚𡭒𢻚𣪒𤸚𥧒𦵚𧤒𨲚𩡒𪯚𫞒𬬚则Ր嘤𐑪%𙊛𚘣𛦩𜕣𝣹𢌣𣚩𤉣𥗩𦆣𧔩𨃣𩑩𪀣𫎩𫽣𭌱𮊉𐠏𘫊𙹒𛇚𛶒𝄚𞂾𡭒𢻚𣪒𤸚𥧒𦵚𧤒𨲚𩡒𪯚𫞒𬬚丱Ր刾𐑪$𙊛𚘣𛦩𜕣𝣪🠱𢌣𣚩𤉣𥗩𦆣𧔩𨃣𩑩𪀣𫎩𫽣𭌱𮙱𐠏𘫊𙹒𛇚𛶖𞂾𡭒𢻚𣪒𤸚𥧒𦵚𧤒𨲚𩡒𪯚𫞒𬬚䩉Ր乘𐑪#𙊛𚘣𛦩𝔃🠱𢌣𣚩𤉣𥗩𦆣𧔩𨃣𩑩𪀣𫎩𫽣𭌱𮩙𐠏𘫊𙹒𛇚𛶒𡼺𢻙𣹺𤸙𥶺𦵙𧳺𨲙𩰺𪯙𫭺𬬙䙡Ր䩲𐑪"贈𙊛𚘣𛦩𜕷𢜊𣋃𤙊𥈃𦖊𧅃𨓊𩂃𪐊𪿃𬍊𬽊𮹁𐠏𘫊𚈽𛶒𢌣𤉣𦆣𨃣𪀣𫽣䉹敏Ր䚌𐑪!﹌𙊜𛗂𜕸𢻝𤸝𦵝𨲝𪯝𬭣𯈩㺑︩Ր䊦𐑪 𐋐𯘑㪩煙켙𐈑𰶄𴰄𸪄Ր㺝畗팊𐑪𐙽𱴬𵮬𹨶䩶῾𰶄𴰄𸪄Ȏ꿝㛁浳쬳𐗹𰦙𱴡𴠙𵮡𸚙𹨡Ր㪵礶썢훲𐑪𐩣𲄒𵾒𹸝𯷡῾𰦞𴠞𸚞Ȏ꯹㋙浳켚𐧡𰇊𲄉𴁊𵾉𷻊𹸉Ր㛎礵훳𐑪𐹈𲓷𶍷𺈄𰇉῾𰇐𴁐𷻐䕏랪썡ϻ꯳뽹⻱浳쬳𐷉𯷡𲄉𲣙𳱡𵾉𶝙𷫡𹸉𺗙Ր㋧礵읉훴𐑪𑈮𲓱𲳄𶍱𶭄𺇱𺧒𰖱῾𰇑𲣙𴁑𶝙𷻑𺗙䕏꯱돃썣ϻꠉ꿙뽹⬉憺浳켚𑆱𯷡𲓱𲳁𳱡𶍱𶭁𷫡𺇱𺧁Ր⻽榉礴훵𐑪𑘕𳂫𶼫𺶹𰦙῾𰇎𱴥𴁎𵮥𷻎𹨥䕏꯱랫읋ϻꠉ꿚썡✡憺煙𑖙𯷡𳂩𳱡𶼩𷫡𺶩Ր⬖榊畍팏𱤹𵞹𹘹𐑪𑧼𳒒𷌒𻆠𰶁῾𯷣𱅫𲄌𳱣𴿫𵾌𷫣𸹫𹸌䕏꿜ϻꠊ뽼⌹憺𑦁䩶𳂩𳡹𶼩𷛹𺶩Ր✯榘켩𰦚𱴡𴠚𵮡𸚚𹨡𐑪𑷢𳒑𷌑𻆠𱅩῾𩐊𰦢𳡻𴠢𷛻𸚢䕏꿟ὑ憺𑵩𯘑𳂪𶼪𺶩Ր⍈榚쭃𰖱𴐱𸊱𐑪𒇈𻆠𱕑῾𯙀Ȏ돁ϻ꯲랫᭩𒅑𮩛𻆑𻵉Րὴ썶𐑪𒖬𻕺𼄼𱤹῾𮪋𻵉Ȏ돁뽹ϻꠋ랪썣ខ𒔹𮙱𻆑𻥡𼄱Րᮌ켬𐑪𒦒𻕹𼔣𱴡῾𮚥𻥢Ȏ도ϻꐤ썤᎙𒤡𮊉𻕹𼄱Րឤ팔𐑪𒵸𼔣𲄉῾𮋁Ȏ꿙랪썡ϻ꯱읉䕏ꐢ돁뽹쬲ྱ𒴉𼄱𼤁ՐᎽ팕𐑪𓅟𼔙𼳱𲓱῾𮋂𼤁Ȏ꿞䕏ꐣ읋௉𓃱𭪺𼔙𼳩Ր࿖팖𐑪𓕄𽃘𲣙῾𭫶Ȏ꯸䕏ꐢ쬲ߡ𓓙𭛑𼳩Ր௯팗𐑪𓤪𽃘𲳁῾𭫶Ȏ꯳뽻Ϲ𓣁𭛑𼳩Րࠊ랪쭊𐑪𓴑𽃘𳂩῾𭻜ϻꠋ썣𐑪𔃹𼳱ՐТ도켲𓲩𭪹𼤁𳒑ϻꐤ썤⌹憹ꀹ𒔹𖎹𚈹𞂹𡼹𥶹𩰹𭪹𱤹𵞹𹘹𽒹뛌Ѐ⬌䊀榌脀돁뽹팃𐘀𒴌𔒀𖮌𘌀𚨌𜆀𞢌𠀀𢜌𣺀𦖌𧴀𪐌𫮀𮊌頩𲄌𳢀𵾌𷜀𹸌𻖀𽲌ጉ✡㪪斡礪랪︪𒤡𓲪𖞡𗬪𚘡𛦪𞒡🠪𢌡𣚪𦆡𧔪𪀡𫎪𭺡𯈪𱴡𳂪𵮡𶼪𹨡𺶪𽢡𾰩𳡻⌹㪩憹礩ꀹ랩︩𒔹𓲩𖎹𗬩𚈹𛦩𞂹🠩𡼹𣚩𥶹𧔩𩰹𫎩𭪹𯈩𱤹𳂩𵞹𶼩𹘹𺶩𽒹𾰩ጉЀ⬌䊀榌脀ꠌ뾀𐘀𒴌𔒀𖮌𘌀𚨌𜆀𞢌𠀀𢜌𣺀𦖌𧴀𪐌𫮀𮊌頩𲄌𳢀𵾌𷜀𹸌𻖀𽲌뛌✡㺑斡紑ꐡ뮑𐈑𒤡𔂑𖞡𗼑𚘡𛶑𞒡🰑𢌡𣪑𦆡𧤑𪀡𫞑𭺡𯘑𱴡𳒑𵮡𷌑𹨡𻆑𽢡𴁉뛌𴐱⌹⬉㪩憹榉礩ꀹꠉ랩︩𒔹𒴉𓲩𖎹𖮉𗬩𚈹𚨉𛦩𞂹𞢉🠩𡼹𢜉𣚩𥶹𦖉𧔩𩰹𪐉𫎩𭪹𮊉𯈩𱤹𲄉𳂩𵞹𵾉𶼩𹘹𹸉𺶩𽒹𽲉𾰩ጉЀ⻳䊀浳脀꯳뾀𐘀𓃳𔒀𖽳𘌀𚷳𜆀𞱳𠀀𢫳𣺀𦥳𧴀𪟳𫮀𮙳頩𲓳𳢀𶍳𷜀𺇳𻖀𾁳뛌✡㺑斡紑ꐡ뮑𐈑𒤡𔂑𖞡𗼑𚘡𛶑𞒡🰑𢌡𣪑𦆡𧤑𪀡𫞑𭺡𯘑𱴡𳒑𵮡𷌑𹨡𻆑𽢡𴠙⌹⬌憹榌ꀹꠌ𒔹𒴌𖎹𖮌𚈹𚨌𞂹𞢌𡼹𢜌𥶹𦖌𩰹𪐌𭪹𮊌𱤹𲄌𵞹𵾌𹘹𹸌𽒹𽲌ጉЀ✡㪩䊀斡礩脀ꐡ랩뾀︩𐘀𒤡𓲩𔒀𖞡𗬩𘌀𚘡𛦩𜆀𞒡🠩𠀀𢌡𣚩𣺀𦆡𧔩𧴀𪀡𫎩𫮀𭺡𯈩頩𱴡𳂩𳢀𵮡𶼩𷜀𹨡𺶩𻖀𽢡𾰩뛌㺑紑뮑𐈑𔂑𗼑𛶑🰑𣪑𧤑𫞑𯘑𳒑𷌑𻆑𴰁⌹㪩憹礩ꀹ랩︩𒔹𓲩𖎹𗬩𚈹𛦩𞂹🠩𡼹𣚩𥶹𧔩𩰹𫎩𭪹𯈩𱤹𳂩𵞹𶼩𹘹𺶩𽒹𾰩ጉЀ䊀脀뾀𐘀𔒀𘌀𜆀𠀀𣺀𧴀𫮀頩𳢀𷜀𻖀뛌✥㺑斥紑ꐥ뮑𐈑𒤥𔂑𖞥𗼑𚘥𛶑𞒥🰑𢌥𣪑𦆥𧤑𪀥𫞑𭺥𯘑𱴥𳒑𵮥𷌑𹨥𻆑𽢥𴿫⌹㪩憹礩ꀹ랩︩𒔹𓲩𖎹𗬩𚈹𛦩𞂹🠩𡼹𣚩𥶹𧔩𩰹𫎩𭪹𯈩𱤹𳂩𵞹𶼩𹘹𺶩𽒹𾰩ጉЀ⬌䊀榌脀ꠌ뾀𐘀𒴌𔒀𖮌𘌀𚨌𜆀𞢌𠀀𢜌𣺀𦖌𧴀𪐌𫮀𮊌頩𲄌𳢀𵾌𷜀𹸌𻖀𽲌뛌✡㺑斡紑ꐡ뮑𐈑𒤡𔂑𖞡𗼑𚘡𛶑𞒡🰑𢌡𣪑𦆡𧤑𪀡𫞑𭺡𯘑𱴡𳒑𵮡𷌑𹨡𻆑𽢡𵞹뛌𵮡뛌⌹憹ꀹ𒔹𖎹𚈹𞂹𡼹𥶹𩰹𭪹𱤹𵞹𹘹𽒹ጉߦ✥䙦斥蓦ꐥ썦𐧦𒤥𔡦𖞥𘛦𚘥𜕦𞒥𠏦𢌥𤉦𦆥𨃦𪀥𫽦𭺥𯷦𱴥𳱦𵮥𷫦𹨥𻥦𽢥ὑ㪫巑礫鱑랫︫𒅑𓲫𕿑𗬫𙹑𛦫𝳑🠫𡭑𣚫𥧑𧔫𩡑𫎫𭛑𯈫𱕑𳂫𵏑𶼫𹉑𺶫𽃑𾰩𵾉ጉྴ✥临斥貴ꐥ쬴𑆴𒤥𕀴𖞥𘺴𚘥𜴴𞒥𠮴𢌥𤨴𦆥𨢴𪀥𬜴𭺥𰖴𱴥𴐴𵮥𸊴𹨥𼄴𽢥ߢὑ㪩䙢巑礩蓢鱑랩썢︩𐧢𒅑𓲩𔡢𕿑𗬩𘛢𙹑𛦩𜕢𝳑🠩𠏢𡭑𣚩𤉢𥧑𧔩𨃢𩡑𫎩𫽢𭛑𯈩𯷢𱕑𳂩𳱢𵏑𶼩𷫢𹉑𺶩𻥢𽃑𾰩뛌⌹㺒憹紒ꀹ뮒𐈒𒔹𔂒𖎹𗼒𚈹𛶒𞂹🰒𡼹𣪒𥶹𧤒𩰹𫞒𭪹𯘒𱤹𳒒𵞹𷌒𹘹𻆒𽒹𶍱ྴ㪩临礩貴랩쬴︩𑆴𓲩𕀴𗬩𘺴𛦩𜴴🠩𠮴𣚩𤨴𧔩𨢴𫎩𬜴𯈩𰖴𳂩𴐴𶼩𸊴𺶩𼄴𾰩ጉϹ⌾䉹憾胹ꀾ뽹𐗹𒔾𔑹𖎾𘋹𚈾𜅹𞂾🿹𡼾𣹹𥶾𧳹𩰾𫭹𭪾䩶𱤾𳡹𵞾𷛹𹘾𻕹𽒾뛌ߢὑ㺑䙢巑紑蓢鱑뮑썢𐈑𐧢𒅑𔂑𔡢𕿑𗼑𘛢𙹑𛶑𜕢𝳑🰑𠏢𡭑𣪑𤉢𥧑𧤑𨃢𩡑𫞑𫽢𭛑𯘑𯷢𱕑𳒑𳱢𵏑𷌑𷫢𹉑𻆑𻥢𽃑𶝙᭩㪩姩礩顩랩훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𡝩𣚩𥗩𧔩𩑩𫎩𭋩𯈩𱅩𳂩𴿩𶼩𸹩𺶩𼳩𾰩ጉϻ⌾䉻憾胻ꀾ뽻𐗻𒔾𔑻𖎾𘋻𚈾𜅻𞂾🿻𡼾𣹻𥶾𧳻𩰾𫭻𭪾𩐊𱤾𳡻𵞾𷛻𹘾𻕻𽒾뛌ླὑ㺑丳巑紑貳鱑뮑쬳𐈑𑆳𒅑𔂑𕀳𕿑𗼑𘺳𙹑𛶑𜴳𝳑🰑𠮳𡭑𣪑𤨳𥧑𧤑𨢳𩡑𫞑𬜳𭛑𯘑𰖳𱕑𳒑𴐳𵏑𷌑𸊳𹉑𻆑𼄳𽃑𶭁᭩㛂姩畂顩돂훩既𑵩𓣂𕯩𗝂𙩩𛗂𝣩👂𡝩𣋂𥗩𧅂𩑩𪿂𭋩𮹂𱅩𲳂𴿩𶭂𸹩𺧂𼳩𾡂ጉϾ⌽䉾憽胾ꀽ뽾𐗾𒔽𔑾𖎽𘋾𚈽𜅾𞂽🿾𡼽𣹾𥶽𧳾𩰽𫭾𭪽頋𱤽𳡾𵞽𷛾𹘽𻕾𽒽뛌ὑ㺑巑紑鱑뮑𐈑𒅑𔂑𕿑𗼑𙹑𛶑𝳑🰑𡭑𣪑𥧑𧤑𩡑𫞑𭛑𯘑𱕑𳒑𵏑𷌑𹉑𻆑𽃑𶼩뛌ὑ巑鱑𒅑𕿑𙹑𝳑𡭑𥧑𩡑𭛑𱕑𵏑𹉑𽃑Ͼ⌾䉾憾胾ꀾ뽾𐗾𒔾𔑾𖎾𘋾𚈾𜅾𞂾🿾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𱤾𳡾𵞾𷛾𹘾𻕾𽒾ጉ᭩㪪姩礪顩랪훩︪𑵩𓲪𕯩𗬪𙩩𛦪𝣩🠪𡝩𣚪𥗩𧔪𩑩𫎪𭋩𯈪𱅩𳂪𴿩𶼪𸹩𺶪𼳩𾰩𷌑⌹憹ꀹ𒔹𖎹𚈹𞂹𡼹𥶹𩰹𭪹𱤹𵞹𹘹𽒹뛌Ѐ⬌䊀榌脀ꠌ뾀𐘀𒴌𔒀𖮌𘌀𚨌𜆀𞢌𠀀𢜌𣺀𦖌𧴀𪐌𫮀𮊌頩𲄌𳢀𵾌𷜀𹸌𻖀𽲌ጉ✡㪪斡礪ꐡ랪︪𒤡𓲪𖞡𗬪𚘡𛦪𞒡🠪𢌡𣚪𦆡𧔪𪀡𫎪𭺡𯈪𱴡𳂪𵮡𶼪𹨡𺶪𽢡𾰩𷛻⌹㪩憹礩ꀹ랩︩𒔹𓲩𖎹𗬩𚈹𛦩𞂹🠩𡼹𣚩𥶹𧔩𩰹𫎩𭪹𯈩𱤹𳂩𵞹𶼩𹘹𺶩𽒹𾰩ጉЀ⬌䊀榌脀ꠌ뾀𐘀𒴌𔒀𖮌𘌀𚨌𜆀𞢌𠀀𢜌𣺀𦖌𧴀𪐌𫮀𮊌頩𲄌𳢀𵾌𷜀𹸌𻖀𽲌뛌✡㺑斡紑ꐡ뮑𐈑𒤡𔂑𖞡𗼑𚘡𛶑𞒡🰑𢌡𣪑𦆡𧤑𪀡𫞑𭺡𯘑𱴡𳒑𵮡𷌑𹨡𻆑𽢡𷻉뛌𸊱⌹⬉㪩憹榉礩ꀹꠉ랩︩𒔹𒴉𓲩𖎹𖮉𗬩𚈹𚨉𛦩𞂹𞢉🠩𡼹𢜉𣚩𥶹𦖉𧔩𩰹𪐉𫎩𭪹𮊉𯈩𱤹𲄉𳂩𵞹𵾉𶼩𹘹𹸉𺶩𽒹𽲉𾰩ጉЀ⻳䊀浳脀꯳뾀𐘀𓃳𔒀𖽳𘌀𚷳𜆀𞱳𠀀𢫳𣺀𦥳𧴀𪟳𫮀𮙳頩𲓳𳢀𶍳𷜀𺇳𻖀𾁳뛌✡㺑斡紑ꐡ뮑𐈑𒤡𔂑𖞡𗼑𚘡𛶑𞒡🰑𢌡𣪑𦆡𧤑𪀡𫞑𭺡𯘑𱴡𳒑𵮡𷌑𹨡𻆑𽢡𸚙⌹⬌憹榌ꀹꠌ𒔹𒴌𖎹𖮌𚈹𚨌𞂹𞢌𡼹𢜌𥶹𦖌𩰹𪐌𭪹𮊌𱤹𲄌𵞹𵾌𹘹𹸌𽒹𽲌ጉЀ✡㪩䊀斡礩脀ꐡ랩뾀︩𐘀𒤡𓲩𔒀𖞡𗬩𘌀𚘡𛦩𜆀𞒡🠩𠀀𢌡𣚩𣺀𦆡𧔩𧴀𪀡𫎩𫮀𭺡𯈩頩𱴡𳂩𳢀𵮡𶼩𷜀𹨡𺶩𻖀𽢡𾰩뛌㺑紑뮑𐈑𔂑𗼑𛶑🰑𣪑𧤑𫞑𯘑𳒑𷌑𻆑𸪁⌹㪩憹礩ꀹ랩︩𒔹𓲩𖎹𗬩𚈹𛦩𞂹🠩𡼹𣚩𥶹𧔩𩰹𫎩𭪹𯈩𱤹𳂩𵞹𶼩𹘹𺶩𽒹𾰩ጉЀ䊀脀뾀𐘀𔒀𘌀𜆀𠀀𣺀𧴀𫮀頩𳢀𷜀𻖀뛌✥㺑斥紑ꐥ뮑𐈑𒤥𔂑𖞥𗼑𚘥𛶑𞒥🰑𢌥𣪑𦆥𧤑𪀥𫞑𭺥𯘑𱴥𳒑𵮥𷌑𹨥𻆑𽢥𸹫⌹㪩憹礩ꀹ랩︩𒔹𓲩𖎹𗬩𚈹𛦩𞂹🠩𡼹𣚩𥶹𧔩𩰹𫎩𭪹𯈩𱤹𳂩𵞹𶼩𹘹𺶩𽒹𾰩ጉЀ⬌䊀榌脀ꠌ뾀𐘀𒴌𔒀𖮌𘌀𚨌𜆀𞢌𠀀𢜌𣺀𦖌𧴀𪐌𫮀𮊌頩𲄌𳢀𵾌𷜀𹸌𻖀𽲌뛌✡㺑斡紑ꐡ뮑𐈑𒤡𔂑𖞡𗼑𚘡𛶑𞒡🰑𢌡𣪑𦆡𧤑𪀡𫞑𭺡𯘑𱴡𳒑𵮡𷌑𹨡𻆑𽢡𹘹뛌𹨡뛌⌹憹ꀹ𒔹𖎹𚈹𞂹𡼹𥶹𩰹𭪹𱤹𵞹𹘹𽒹ጉߦ✥䙦斥蓦ꐥ썦𐧦𒤥𔡦𖞥𘛦𚘥𜕦𞒥𠏦𢌥𤉦𦆥𨃦𪀥𫽦𭺥𯷦𱴥𳱦𵮥𷫦𹨥𻥦𽢥ὑ㪫巑礫鱑랫︫𒅑𓲫𕿑𗬫𙹑𛦫𝳑🠫𡭑𣚫𥧑𧔫𩡑𫎫𭛑𯈫𱕑𳂫𵏑𶼫𹉑𺶫𽃑𾰩𹸉ጉྴ✥临斥貴ꐥ쬴𑆴𒤥𕀴𖞥𘺴𚘥𜴴𞒥𠮴𢌥𤨴𦆥𨢴𪀥𬜴𭺥𰖴𱴥𴐴𵮥𸊴𹨥𼄴𽢥ߢὑ㪩䙢巑礩蓢鱑랩썢︩𐧢𒅑𓲩𔡢𕿑𗬩𘛢𙹑𛦩𜕢𝳑🠩𠏢𡭑𣚩𤉢𥧑𧔩𨃢𩡑𫎩𫽢𭛑𯈩𯷢𱕑𳂩𳱢𵏑𶼩𷫢𹉑𺶩𻥢𽃑𾰩뛌⌹㺒憹紒ꀹ뮒𐈒𒔹𔂒𖎹𗼒𚈹𛶒𞂹🰒𡼹𣪒𥶹𧤒𩰹𫞒𭪹𯘒𱤹𳒒𵞹𷌒𹘹𻆒𽒹𺇱ྴ㪩临礩貴랩쬴︩𑆴𓲩𕀴𗬩𘺴𛦩𜴴🠩𠮴𣚩𤨴𧔩𨢴𫎩𬜴𯈩𰖴𳂩𴐴𶼩𸊴𺶩𼄴𾰩ጉϹ⌾䉹憾胹ꀾ뽹𐗹𒔾𔑹𖎾𘋹𚈾𜅹𞂾🿹𡼾𣹹𥶾𧳹𩰾𫭹𭪾䩶𱤾𳡹𵞾𷛹𹘾𻕹𽒾뛌ߢὑ㺑䙢巑紑蓢鱑뮑썢𐈑𐧢𒅑𔂑𔡢𕿑𗼑𘛢𙹑𛶑𜕢𝳑🰑𠏢𡭑𣪑𤉢𥧑𧤑𨃢𩡑𫞑𫽢𭛑𯘑𯷢𱕑𳒑𳱢𵏑𷌑𷫢𹉑𻆑𻥢𽃑𺗙᭩㪩姩礩顩랩훩︩𑵩𓲩𕯩𗬩𙩩𛦩𝣩🠩𡝩𣚩𥗩𧔩𩑩𫎩𭋩𯈩𱅩𳂩𴿩𶼩𸹩𺶩𼳩𾰩ጉϻ⌾䉻憾胻ꀾ뽻𐗻𒔾𔑻𖎾𘋻𚈾𜅻𞂾🿻𡼾𣹻𥶾𧳻𩰾𫭻𭪾𩐊𱤾𳡻𵞾𷛻𹘾𻕻𽒾뛌ླὑ㺑丳巑紑貳鱑뮑쬳𐈑𑆳𒅑𔂑𕀳𕿑𗼑𘺳𙹑𛶑𜴳𝳑🰑𠮳𡭑𣪑𤨳𥧑𧤑𨢳𩡑𫞑𬜳𭛑𯘑𰖳𱕑𳒑𴐳𵏑𷌑𸊳𹉑𻆑𼄳𽃑𺧁᭩㛂姩畂顩돂훩既𑵩𓣂𕯩𗝂𙩩𛗂𝣩👂𡝩𣋂𥗩𧅂𩑩𪿂𭋩𮹂𱅩𲳂𴿩𶭂𸹩𺧂𼳩𾡂ጉϾ⌽䉾憽胾ꀽ뽾𐗾𒔽𔑾𖎽𘋾𚈽𜅾𞂽🿾𡼽𣹾𥶽𧳾𩰽𫭾𭪽頋𱤽𳡾𵞽𷛾𹘽𻕾𽒽뛌ὑ㺑巑紑鱑뮑𐈑𒅑𔂑𕿑𗼑𙹑𛶑𝳑🰑𡭑𣪑𥧑𧤑𩡑𫞑𭛑𯘑𱕑𳒑𵏑𷌑𹉑𻆑𽃑𺧀ÿ뛌ὑ巑鱑𒅑𕿑𙹑𝳑𡭑𥧑𩡑𭛑𱕑𵏑𹉑𽃑Ͼ⌾䉾憾胾ꀾ뽾𐗾𒔾𔑾𖎾𘋾𚈾𜅾𞂾🿾𡼾𣹾𥶾𧳾𩰾𫭾𭪾頋𱤾𳡾𵞾𷛾𹘾𻕾𽒾ጉ᭩㪪姩礪顩랪훩︪𑵩𓲪𕯩𗬪𙩩𛦪𝣩🠪𡝩𣚪𥗩𧔪𩑩𫎪𭋩𯈪𱅩𳂪𴿩𶼪𸹩𺶪𼳩𾰩"""
    advanced_display_strategy.update_canvas(message=message,
                                            canvas=current_state_constructed_by_message)
    cv2.imshow("Current state constructed by message", current_state_constructed_by_message)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return




def test_rgb_utf8_conversion():
    # Test case 0: Red color
    original_rgb_0 = (255, 0, 0)
    stable_rgb_values_0 = get_stable_rgb_values(*original_rgb_0)
    utf8_char_0 = rgb_to_utf8(*stable_rgb_values_0)
    rgb_tuple_0 = utf8_to_rgb(utf8_char_0)
    assert rgb_tuple_0 == stable_rgb_values_0, f"Test case 0 failed. Expected {stable_rgb_values_0}, got {rgb_tuple_0}"

    # Test case 1: Green color
    original_rgb_1 = (0, 255, 0)
    stable_rgb_values_1 = get_stable_rgb_values(*original_rgb_1)
    utf8_char_1 = rgb_to_utf8(*stable_rgb_values_1)
    rgb_tuple_1 = utf8_to_rgb(utf8_char_1)
    assert rgb_tuple_1 == stable_rgb_values_1, f"Test case 1 failed. Expected {stable_rgb_values_1}, got {rgb_tuple_1}"

    # Test case 2: Blue color
    original_rgb_2 = (0, 0, 255)
    stable_rgb_values_2 = get_stable_rgb_values(*original_rgb_2)
    utf8_char_2 = rgb_to_utf8(*stable_rgb_values_2)
    rgb_tuple_2 = utf8_to_rgb(utf8_char_2)
    assert rgb_tuple_2 == stable_rgb_values_2, f"Test case 2 failed. Expected {stable_rgb_values_2}, got {rgb_tuple_2}"

    # Test case 3: Custom color
    original_rgb_3 = (128, 64, 192)
    stable_rgb_values_3 = get_stable_rgb_values(*original_rgb_3)
    utf8_char_3 = rgb_to_utf8(*stable_rgb_values_3)
    rgb_tuple_3 = utf8_to_rgb(utf8_char_3)
    assert rgb_tuple_3 == stable_rgb_values_3, f"Test case 3 failed. Expected {stable_rgb_values_3}, got {rgb_tuple_3}"

    return






def test_unicode_utf8_conversion():
    # Convert Unicode codepoint to UTF-8 char
    codepoint1 = 990
    utf8_char = chr(codepoint1)
    print(utf8_char)  # Output: Ϟ

    # Convert UTF-8 char to Unicode codepoint
    utf8_char = "Ϟ"
    codepoint2 = ord(utf8_char)
    print(codepoint2)  # Output: 990
    assert codepoint1 == codepoint2




def test_smb_title_demo_messages():
    # Run this with -s
    # a to move to prev frame, s to move to next frame. esc key to quit.
    messages = load_json_file("./files/smb_title_demo_messages.json")
    viewer = MessageViewer(messages)
    viewer.start()
    return


def test_smb_title_demo_messages_artifacting_debug():
    # Run this with -s
    # a to move to prev frame, s to move to next frame. esc key to quit.
    messages = load_json_file("./files/smb_title_demo_messages.json")
    viewer = MessageViewer(messages,
                           cycle_mode=True,
                           start_index=72,
                           end_index=115
                           )
    viewer.start()
    return


def test_smb_title_demo_messages_artifacting_debug_2():
    # Run this with -s
    # a to move to prev frame, s to move to next frame. esc key to quit.
    messages = load_json_file("./files/smb_title_demo_messages.json")
    viewer = MessageViewer(messages,
                           display_canvas_every_update=True,
                           cycle_mode=True,
                           start_index=76,
                           end_index=100
                           )
    viewer.start()
    return
