# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# converters.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import weka.core.jvm as jvm
from weka.core.classes import OptionHandler
from weka.core.capabilities import Capabilities
from weka.core.dataset import Instances
import weka.core.utils as utils


class Loader(OptionHandler):
    """
    Wrapper class for Loaders.
    """
    
    def __init__(self, classname="weka.core.converters.ArffLoader", jobject=None):
        """
        Initializes the specified loader either using the classname or the JB_Object.
        :param classname: the classname of the loader
        :param jobject: the JB_Object to use
        """
        if jobject is None:
            jobject = Loader.new_instance(classname)
        if classname is None:
            classname = utils.get_classname(jobject)
        self.enforce_type(jobject, "weka.core.converters.Loader")
        super(Loader, self).__init__(jobject)

    def load_file(self, dfile):
        """
        Loads the specified file and returns the Instances object.
        :param dfile: the file to load
        """
        self.enforce_type(self.jobject, "weka.core.converters.FileSourcedConverter")
        if not javabridge.is_instance_of(dfile, "Ljava/io/File;"):
            dfile = javabridge.make_instance("Ljava/io/File;", "(Ljava/lang/String;)V", jvm.ENV.new_string_utf(str(dfile)))
        javabridge.call(self.jobject, "reset", "()V")
        javabridge.call(self.jobject, "setFile", "(Ljava/io/File;)V", dfile)
        return Instances(javabridge.call(self.jobject, "getDataSet", "()Lweka/core/Instances;"))
        
    def load_url(self, url):
        """
        Loads the specified URL and returns the Instances object.
        :param url: the URL to load the data from
        """
        self.enforce_type(self.jobject, "weka.core.converters.URLSourcedLoader")
        javabridge.call(self.jobject, "reset", "()V")
        javabridge.call(self.jobject, "setURL", "(Ljava/lang/String;)V", str(url))
        return Instances(javabridge.call(self.jobject, "getDataSet", "()Lweka/core/Instances;"))


class Saver(OptionHandler):
    """
    Wrapper class for Savers.
    """
    
    def __init__(self, classname="weka.core.converters.ArffSaver", jobject=None):
        """
        Initializes the specified saver either using the classname or the provided JB_Object.
        :param classname: the classname of the saver
        :param jobject: the JB_Object to use
        """
        if jobject is None:
            jobject = Saver.new_instance(classname)
        if classname is None:
            classname = utils.get_classname(jobject)
        self.enforce_type(jobject, "weka.core.converters.Saver")
        super(Saver, self).__init__(jobject)

    def get_capabilities(self):
        """
        Returns the capabilities of the saver.
        :rtype: Capabilities
        """
        return Capabilities(javabridge.call(self.jobject, "getCapabilities", "()Lweka/core/Capabilities;"))

    def save_file(self, data, dfile):
        """
        Saves the Instances object in the specified file.
        :param data: the data to save
        :param dfile: the file to save the data to
        """
        self.enforce_type(self.jobject, "weka.core.converters.FileSourcedConverter")
        if not javabridge.is_instance_of(dfile, "Ljava/io/File;"):
            dfile = javabridge.make_instance("Ljava/io/File;", "(Ljava/lang/String;)V", jvm.ENV.new_string_utf(str(dfile)))
        javabridge.call(self.jobject, "setFile", "(Ljava/io/File;)V", dfile)
        javabridge.call(self.jobject, "setInstances", "(Lweka/core/Instances;)V", data.jobject)
        javabridge.call(self.jobject, "writeBatch", "()V")


def loader_for_file(filename):
    """
    Returns a Loader that can load the specified file, based on the file extension. None if failed to determine.
    :param filename: the filename to get the loader for
    :rtype: Loader
    """
    loader = javabridge.static_call(
        "weka/core/converters/ConverterUtils", "getLoaderForFile",
        "(Ljava/lang/String;)Lweka/core/converters/AbstractFileLoader;", filename)
    if loader is None:
        return None
    else:
        return Loader(jobject=loader)


def saver_for_file(filename):
    """
    Returns a Saver that can load the specified file, based on the file extension. None if failed to determine.
    :param filename: the filename to get the saver for
    :rtype: Saver
    """
    saver = javabridge.static_call(
        "weka/core/converters/ConverterUtils", "getSaverForFile",
        "(Ljava/lang/String;)Lweka/core/converters/AbstractFileSaver;", filename)
    if saver is None:
        return None
    else:
        return Saver(jobject=saver)
