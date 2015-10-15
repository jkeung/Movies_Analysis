import os
import luigi
import util

OUTPUTDIR = 'output'
FILENAMETEMPLATE = 'movie_dictionary'

class GetDataForLetter(luigi.Task):
	letter = luigi.Parameter()
	
	def requires(self):
		""" Upstream Tasks required for completion """
		return None

	def run(self):
		""" Runs a job """
		url_list = util.get_movie_url_list(self.letter)
		output_path = os.path.join(OUTPUTDIR, '{0}_{1}.p'.format(FILENAMETEMPLATE, self.letter))
		util.update_movie_dictionary(output_path, url_list)

	def output(self):
		""" Checks for output to see if the task is complete """
		return luigi.LocalTarget(os.path.join(OUTPUTDIR, '{0}_{1}.p'.format(FILENAMETEMPLATE, self.letter)))

class RunManyLetters(luigi.Task):

	def requires(self):
		""" Upstream Tasks required for completion """
		for myletter in '#ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			yield GetDataForLetter(letter = myletter)

if __name__ == "__main__":
	luigi.run(main_task_cls=RunManyLetters)
