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


# logical connectives.



class Or(Sentence):
      def __init__(self, *predicates):
            for predicate in predicates:
                  Sentence.validate(predicate)
            self.predicates = list(predicates)
      

      def __eq__(self,other):
            return isinstance(other,Or) and self.predicates==other.predicates

      def __hash__(self,other):
            return isinstance(other, Or) and self.predicates==other.predicates
      
      def __hash__(self):
        return hash(
            ("or", tuple(hash(predicate) for predicate in self.predicates))
        )
 
      def __repr__(self):
            predicates = ", ".join([str(predicate) for predicate in self.predicates])
            return f"Or({predicates})"
      
      def evaluate(self, model):
            return any(predicate.evaluate(model) for predicate in self.predicates)
      
      def formula(self):
            if len(self.predicates) == 1:
                  return self.predicates[0].formula()
            return " ∨  ".join([Sentence.parenthesize(predicate.formula())
                              for predicate in self.predicates])
      
      def symbols(self):
            return set.union(*[predicate.symbols() for predicate in self.predicates])
      
 
class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent
 
    def __eq__(self, other):
        return (isinstance(other, Implication)
                and self.antecedent == other.antecedent
                and self.consequent == other.consequent)
 
    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))
 
    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"
 
    def evaluate(self, model):
        return ((not self.antecedent.evaluate(model))
                or self.consequent.evaluate(model))
 
    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"
 
    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())
 
 
class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right
 
    def __eq__(self, other):
        return (isinstance(other, Biconditional)
                and self.left == other.left
                and self.right == other.right)
 
    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))
 
    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"
 
    def evaluate(self, model):
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))
 
    def formula(self):
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"
 
    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())
 
 
def model_check(knowledge, query):
    """Checks if knowledge base entails query."""
 
    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""
 
        # If model has an assignment for each symbol
        if not symbols:
 
            # If knowledge base is true in model, then query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:
 
            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()
 
            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True
 
            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False
 
            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))
 
    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())
 
    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())
