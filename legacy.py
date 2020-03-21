## @file

## core AST class
class AST:
    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.val = V
        self.nest = []
        self.attr = {}
        self.rid = id(self)

    def __repr__(self):
        return self.dump()

    def dump(self, depth=0, prefix=''):
        tree = self.pad(depth) + self.head(prefix)
        for i in self.attr:
            tree += self.attr[i].dump(depth + 1, prefix='%s = ' % i)
        for j in self.nest:
            tree += j.dump(depth + 1)
        return tree

    def head(self, prefix=''):
        return '%s<%s:%s> @%i/%i' % (prefix, self.type, self.val, id(self), self.rid)

    def pad(self, depth):
        return '\n' + '\t' * depth

    def __getitem__(self, key):
        return self.attr[key]

    def __setitem__(self, key, that):
        self.attr[key] = that
        return self

    def __lshift__(self, that):
        self[that.type] = that
        return self

    def __rshift__(self, that):
        self[that.val] = that
        return self

    def __floordiv__(self, that):
        self.nest.append(that)
        return self

## function arguments container
class Tuple(AST):
    pass

## C types
class Type(AST):
    pass

## `int`
class Int(Type):
    pass

## `char`
class Char(Type):
    pass

## pointer
class Ptr(Type):
    def __init__(self, V):
        Type.__init__(self, '')
        self // V

## function
class Fn(AST):
    pass

## `return` statement
class Return(AST):
    pass


i32 = Type('int')
main = Fn('main')
main['ret'] = i32
main >> Tuple('args')
main // Return(0)
main['args'] // Int('argc')
main['args'] // Ptr(Ptr(Char('argv')))

print(main)
