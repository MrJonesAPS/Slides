from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.ext import Extension
import re
import os
import pypandoc
import paramiko
import sys
from dotenv import load_dotenv


class RelativeInclude(Extension):
    # This Jinja2 extension Created 2014 by Janusz Skonieczny
    # Source https://gist.github.com/wooyek/8d4c37d684a5ba38b8c1
    """Allows to import relative template names"""
    tags = set(["include2"])

    def __init__(self, environment):
        super(RelativeInclude, self).__init__(environment)
        self.matcher = re.compile("\.*")

    def parse(self, parser):
        node = parser.parse_include()
        template = node.template.as_const()
        if template.startswith("."):
            # determine the number of go ups
            up = len(self.matcher.match(template).group())
            # split the current template name into path elements
            # take elements minus the number of go ups
            seq = parser.name.split("/")[:-up]
            # extend elements with the relative path elements
            seq.extend(template.split("/")[1:])
            template = "/".join(seq)
            node.template.value = template
        return node


# load .env file
load_dotenv()

# setup SFTP connection
host = "whscs.net"  # hard-coded
port = 22
transport = paramiko.Transport((host, port))

# password = os.getenv('MY_PASSWORD')
# username = os.getenv('MY_USERNAME')
password = "ILovKLO!"
username = "mrjones"
transport.connect(username=username, password=password)

sftp = paramiko.SFTPClient.from_transport(transport)

# Setup environment for Jinja
env = Environment(
    loader=FileSystemLoader("templates"),
    extensions=[RelativeInclude],
    trim_blocks=True,
    lstrip_blocks=True,
)

# I can't get the -v/--variable arguments to work
# I know this is bad, but I just manually changed
# these values in the template
pdoc_args = [
    "-s",
    "--include-in-header=style.css",
    "--include-in-header=scripts.html",
    "--template=default_plus_chalkboard.revealjs",
    "--variable=width:1920",
    "--variable=height:1080",
    "--variable=viewDistance:50",
]


slidesToGenerate = []

if "apcsa" in sys.argv:
    slidesToGenerate.append(["APCSA", "AP Computer Science A"])
    print("Generating slides for apcsa")
if "apcsp" in sys.argv:
    slidesToGenerate.append(["APCSP", "AP Computer Science Principles"])
    print("Generating slides for apcsp")
if "prog" in sys.argv:
    slidesToGenerate.append(["programming", "Computer Programming"])
    print("Generating slides for prog")
if "advprog" in sys.argv:
    slidesToGenerate.append(["advprogramming", "Computer Programming, Advanced"])
    print("Generating slides for advprog")

if len(slidesToGenerate) == 0:
    print("received no valid course name arguments, so not generating any slides")


for course, longName in slidesToGenerate:
    for unit in range(10):
        for day in range(10):
            dayTemplateName = (
                "courses/"
                + course
                + "/Unit"
                + str(unit)
                + "/Day"
                + str(day)
                + "/content.md"
            )
            generatedMdFileName = (
                "generated/markdown/"
                + course
                + "/Unit"
                + str(unit)
                + "/Day"
                + str(day)
                + ".md"
            )
            generatedHtmlFileName = (
                "generated/html/"
                + course
                + "/"
                + course
                + "_Unit"
                + str(unit)
                + "_Day"
                + str(day)
                + ".html"
            )
            try:
                template = env.get_template(dayTemplateName)
            except TemplateNotFound:
                # print("cant find " + dayTemplateName)
                continue
            output_from_parsed_template = template.render(
                unit_and_day="Unit " + str(unit) + ", Day " + str(day), course=longName
            )

            # Save the rendered md file to the md folder
            os.makedirs(os.path.dirname(generatedMdFileName), exist_ok=True)
            with open(generatedMdFileName, "w") as fh:
                fh.write(output_from_parsed_template)

            # convert the rendered md file to its final html
            os.makedirs(os.path.dirname(generatedHtmlFileName), exist_ok=True)

            pypandoc.convert_file(
                generatedMdFileName,
                to="revealjs",
                outputfile=generatedHtmlFileName,
                extra_args=pdoc_args,
            )

            # Post slides to website
            path = (
                "/var/www/whscs.net/html/courses/"
                + course
                + "/Unit"
                + str(unit)
                + "/"
                + course
                + "_Unit"
                + str(unit)
                + "_Day"
                + str(day)
                + ".html"
            )
            localpath = generatedHtmlFileName
            print("uploading " + generatedHtmlFileName)
            print("remote filename will be " + path)
            sftp.put(localpath, path)
            # print("success")

if "other" in sys.argv:
    print("generating slides for other")
    # Also generate all the standalone slides in "other"
    for root, dirs, files in os.walk("./templates/courses/Other"):
        for name in files:
            thisTemplateName = "courses/Other/" + name
            generatedMdFileName = "generated/markdown/Other/" + name
            generatedHtmlFileName = "generated/html/Other/" + name.replace(
                ".md", ".html"
            )
            try:
                template = env.get_template(thisTemplateName)
            except TemplateNotFound:
                # print("cant find " + thisTemplateName)
                continue
            output_from_parsed_template = template.render()

            with open(generatedMdFileName, "w") as fh:
                fh.write(output_from_parsed_template)

            pypandoc.convert_file(
                generatedMdFileName,
                to="revealjs",
                outputfile=generatedHtmlFileName,
                extra_args=pdoc_args,
            )

            # Post slides to website
            path = "/var/www/whscs.net/html/courses/Other/" + name.replace(
                ".md", ".html"
            )
            localpath = generatedHtmlFileName
            # print("uploading " + generatedHtmlFileName)
            # print("remote filename will be " + path)
            sftp.put(localpath, path)
            # print("success")

if "img" in sys.argv:
    print("Syncing images folder")
    # Also sync everything from the images folder
    for root, dirs, files in os.walk("./templates/images"):
        for name in files:
            localpath = os.path.join(root, name)
            remotepath = "/var/www/whscs.net/html/courses/images/" + name
            # TODO - how do I only sync new files?
            sftp.put(localpath, remotepath)

sftp.close()
transport.close()
# print('Upload done.')
