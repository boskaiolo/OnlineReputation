import os
import git
import cPickle


class Namer:

    def downloadNames(self):
        repo_name = "git://github.com/dapplebeforedawn/Names.git"
        print "Cloning repository with names: " + repo_name
        workingGit = git.Git(working_dir="../db/")

        try:
            workingGit.clone(repo_name)
        except git.exc.GitCommandError as e:
            print "[GIT EXCEPTION]: " + str(e)

    def checkFiles(self):
        current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
        db_dir = current_dir + "../db/Names/"
        return os.path.isfile(db_dir + "boynames") and os.path.isfile(db_dir + "girlnames")


    def loadNamesFromFile(self):
        if self.checkFiles():
            fh = open("../db/Names/boynames")
            boynames = fh.readlines()
            fh.close()
            fh = open("../db/Names/girlnames")
            girlnames = fh.readlines()
            fh.close()

            self.namedic = {}

            for name in boynames:
                name = name.lower().replace("\n","")
                self.namedic[name] = "M"

            for name in girlnames:
                name = name.lower().replace("\n","")
                if name not in self.namedic.keys():
                    self.namedic[name] = "F"
                else:
                    # this name is for both male and female
                    del self.namedic[name]

            print "Loaded names:", len(self.namedic)

    def dumpPickle(self):
        current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
        db_dir = current_dir + "../db/"
        with open(db_dir + "names.pickle", "wb") as fid:
            cPickle.dump(self.namedic, fid, protocol=cPickle.HIGHEST_PROTOCOL)

    def loadPickle(self):
        current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
        db_dir = current_dir + "../db/"
        with open(db_dir + "names.pickle", "rb") as fid:
            self.namedic = cPickle.load(fid)

    def checkPickle(self):
        current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
        db_dir = current_dir + "../db/"
        return os.path.isfile(db_dir + "names.pickle")

    def __init__(self):

        if self.checkPickle():
            self.loadPickle()

        elif self.checkFiles():
            self.loadNamesFromFile()
            self.dumpPickle()

        else:
            self.downloadNames()
            self.loadNamesFromFile()
            self.dumpPickle()

    def nameLookup(self, name):
        try:
            return self.namedic[name.lower().strip()]
        except KeyError as e:
            return ""
