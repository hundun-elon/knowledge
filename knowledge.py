import itertools

# blueprint for a logical sentence
class Sentence():
      
      # method to evaluate the truth value of a logical sentence
      def evaluate(self,model):

            raise Exception('nothing to evaluate')
      
      # method to get a set of all symbols in a logical sentence.
      def symbols(self):
            return set()
      
      @classmethod
      def validate(cls, sentence):
            # if we dont pass in a logical sentence.
            if not isinstance(sentence, Sentence):
                  raise TypeError("must be a logical sentence")
            
      
      @classmethod
      def parenthesize(cls,s):
            # method to parenthesize the expression if it not already.
            def balanced(s):
                  # check if the string has valid parenthesis.
                  count =0 
                  for c in s:
                        if c =="(":
                              count+=1
                        elif c==")":
                              if count <=0:
                                    return False
                              count-=1 
                        return count==0
                  

            if not len(s) or s.isalpha() or (
                  s[0] =="(" and s[-1]==")" and balanced(s[1:-1])
            ):
                  return s 
            else:
                  return f"({s})"
            
# class to represent a logical symbol.

class Symbol(Sentence):

      def __init__(self, name):
            self.name = name 
      
      def __eq__(self,other):
            return isinstance(other,Symbol) and self.name==other.name 
      
           
      def __hash__(self):
            return hash(("Symbol",self.name))
      
      def __repr__(self):
            return self.name 
      
      def evaluate(self,model):

            try:
                  return bool(model[self.name])
            except KeyError:
                  raise EvaluationException(f"variable {self.name} is not in model ")
      
      def formula(self):
            return self.name 
      
      def symbols(self):
            return {self.name}
      