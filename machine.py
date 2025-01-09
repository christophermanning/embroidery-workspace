import math


# Machine-specific configuration
class Machine:
    # this is the average because the machine may automatically
    # adjust the speed for some pattern segments
    stitches_per_second = 10

    # size of the embroidery canvas
    #
    # 1 unit refers to 1/10th of a mm
    width = 1000
    height = 1000

    def humanize_duration(self, num_stitches):
        seconds = num_stitches / self.stitches_per_second
        minutes = math.floor(seconds / 60)
        seconds = int(seconds % 60)

        seconds_text = f"{seconds} second{'s' if seconds != 1 else ''}"
        minutes_text = f"{minutes} minute{'s' if minutes != 1 else ''}"

        parts = []

        if minutes != 0:
            parts.append(minutes_text)

        if seconds != 0 or (minutes == 0 and seconds == 0):
            parts.append(seconds_text)

        return " ".join(parts)
