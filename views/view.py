from flask import render_template

class View:
    def __init__(self):
        self.empty = None

    def render_home(self):
        return render_template('home.html')

    def render_uploading(self, number_video, total_number):
        return render_template('uploading.html', number_video=number_video, total_number=total_number)

    def render_transcribing(self, number_video, total_number, length_dictionary):
        return render_template('transcribing.html', number_video=number_video, total_number=total_number,
                               length_dictionary=length_dictionary)

    def render_finished(self):
        return render_template('finished.html')