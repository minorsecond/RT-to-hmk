import csv
import os

def convert(rt_path, out_path):
    new_file = os.path.normpath(out_path + "\\rt_systems_hmk.hmk")
    hmk_data_header = """KENWOOD MCP FOR AMATEUR MOBILE TRANSCEIVER
[Export Software]=MCP-2A Version 3.20
[Export File Version]=1
[Type]=K
[Language]=English\n
// Comments
!!Comments=\n
// Memory Channels\n"""

    hmk_table_header = ["!!Ch",
                  "Rx Freq.",
                  "Rx Step",
                  "Offset",
                  "T/CT/DCS",
                  "TO Freq.",
                  "CT Freq.",
                  "DCS Code",
                  "Shift/Split",
                  "Rev.",
                  "L.Out",
                  "Mode",
                  "Tx Freq.",
                  "Tx Step",
                  "M.Name"]

    with open(new_file, mode="w", newline="") as out_file:
        out_writer = csv.writer(out_file, delimiter=',')
        out_writer.writerow(hmk_table_header)

        with open(rt_path) as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count > 0:
                    hmk_ch = row[0].rjust(4, '0')
                    hmk_rx_freq = row[1]
                    hmk_rx_step = row[13]
                    hmk_offset = row[3]  # TODO: convert number format

                    tone_mode = row[7]
                    if tone_mode == "None":
                        hmk_TCTDCS = "Off"
                        hmk_to_freq = "100.0"
                        hmk_ct_freq = "100.0"
                        hmk_dcs_code = "023"
                    elif tone_mode == "Tone":
                        hmk_TCTDCS = "CT"
                        hmk_to_freq = row[9]
                        hmk_ct_freq = row[8]
                        hmk_dcs_code = "023"
                    elif tone_mode == "DCS":
                        hmk_TCTDCS = "DCS"
                        hmk_to_freq = "100.0"
                        hmk_ct_freq = "100.0"
                        hmk_dcs_code = row[10]

                    hmk_shift = "+" if float(row[1]) < float(row[2]) else "-"

                    hmk_rev = "Off"
                    hmk_lout = "Off"
                    hmk_mode = row[5]
                    hmk_tx_freq = row[2]
                    hmk_tx_step = row[13]
                    hmk_m_name = row[6]

                    new_row = [hmk_ch,
                               hmk_rx_freq,
                               hmk_rx_step,
                               hmk_offset,
                               hmk_TCTDCS,
                               hmk_to_freq,
                               hmk_ct_freq,
                               hmk_dcs_code,
                               hmk_shift,
                               hmk_rev,
                               hmk_lout,
                               hmk_mode,
                               hmk_tx_freq,
                               hmk_tx_step,
                               hmk_m_name]

                    out_writer.writerow(new_row)

                line_count += 1

    # Write the data header
    with open(new_file, 'r+', newline='') as f:
        content = f.read()
        f.seek(0,0)
        f.write(hmk_data_header + content)

def main():
    rt_systems_file = input("Path to RT Systems CSV Export: ")
    hmk_output_path = os.path.normpath(input("Directory to write HMK file to: "))

    convert(rt_systems_file, hmk_output_path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
