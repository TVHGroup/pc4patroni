'''
Created on 11-feb.-2016

http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes

'''

class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)