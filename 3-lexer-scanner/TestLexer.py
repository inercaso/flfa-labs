import unittest
from Lexer import Lexer
from Tokens import TokenType

class LexerTest(unittest.TestCase):
    def test_basic_notes(self):
        """test basic note tokenization"""
        source = "c d e f g a b"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # check that we have the expected number of tokens (+1 for EOF)
        self.assertEqual(len(tokens), 8)
        
        # check that all tokens are NOTE tokens
        for i in range(7):
            self.assertEqual(tokens[i].type, TokenType.NOTE)
        
        # check note values
        self.assertEqual(tokens[0].value, 'c')
        self.assertEqual(tokens[1].value, 'd')
        self.assertEqual(tokens[2].value, 'e')
        self.assertEqual(tokens[3].value, 'f')
        self.assertEqual(tokens[4].value, 'g')
        self.assertEqual(tokens[5].value, 'a')
        self.assertEqual(tokens[6].value, 'b')
    
    def test_note_modifiers(self):
        """test sharp and flat modifiers"""
        source = "c# d# f# g# a# bb"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # expected pattern: NOTE SHARP NOTE SHARP ...
        self.assertEqual(tokens[0].type, TokenType.NOTE)
        self.assertEqual(tokens[1].type, TokenType.SHARP)
        self.assertEqual(tokens[2].type, TokenType.NOTE)
        self.assertEqual(tokens[3].type, TokenType.SHARP)
    
    def test_durations(self):
        """test note duration tokens"""
        source = "c4 d8 e16 f2 g1"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # expected pattern: NOTE DURATION NOTE DURATION ...
        self.assertEqual(tokens[0].type, TokenType.NOTE)
        self.assertEqual(tokens[1].type, TokenType.DURATION)
        self.assertEqual(tokens[1].value, 4)
        
        self.assertEqual(tokens[2].type, TokenType.NOTE)
        self.assertEqual(tokens[3].type, TokenType.DURATION)
        self.assertEqual(tokens[3].value, 8)
    
    def test_comments(self):
        """test comment handling"""
        source = "c4 // this is a comment\nd4"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # comment should be skipped, resulting in tokens: NOTE DURATION NOTE DURATION EOF
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].type, TokenType.NOTE)
        self.assertEqual(tokens[1].type, TokenType.DURATION)
        self.assertEqual(tokens[2].type, TokenType.NOTE)
        self.assertEqual(tokens[3].type, TokenType.DURATION)
    
    def test_special_commands(self):
        """test special command tokens"""
        source = "\\tempo=120 \\function(transpose, c, 2)"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.COMMAND)
        self.assertEqual(tokens[0].value, "\\tempo")
        self.assertEqual(tokens[1].type, TokenType.EQUALS)
        self.assertEqual(tokens[2].type, TokenType.DURATION)
        self.assertEqual(tokens[2].value, 120)
    
    def test_structure_symbols(self):
        """test music structure symbols"""
        source = "c4 | d4 |: e4 f4 :|"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # find the bar and repeat tokens
        bar_token = None
        repeat_start = None
        repeat_end = None
        
        for token in tokens:
            if token.type == TokenType.BAR:
                bar_token = token
            elif token.type == TokenType.REPEAT_START:
                repeat_start = token
            elif token.type == TokenType.REPEAT_END:
                repeat_end = token
        
        self.assertIsNotNone(bar_token)
        self.assertIsNotNone(repeat_start)
        self.assertIsNotNone(repeat_end)

if __name__ == '__main__':
    unittest.main() 