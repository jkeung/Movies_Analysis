import os
import luigi
import util

class GetDataForLetter(luigi.Task):
	letter = luigi.Parameter()

	def run(self):
		url_list = util.get_movie_url_list(self.letter)
		output_path = os.path.join(util.OUTPUTDIR, '{0}_{1}.p'.format(util.FILENAMETEMPLATE, self.letter))
		util.update_movie_dictionary(output_path, url_list)

	def output(self):
		return luigi.LocalTarget(os.path.join(util.OUTPUTDIR, '{0}_{1}.p'.format(util.FILENAMETEMPLATE, self.letter)))


class RunManyLetters(luigi.Task):
	
	def requires(self):
		for myletter in '#ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			yield GetDataForLetter(letter=myletter)

if __name__ == "__main__":
	luigi.run(main_task_cls=RunManyLetters)
