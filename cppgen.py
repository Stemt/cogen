
class cpp_var:
    def __init__(self,type_name,name):
        self.type_name = type_name
        self.name = name

    def as_def_str(self):
        return "{} {};\n".format(self.type_name, self.name)

    def as_arg_str(self):
        return "{} {}".format(self.type_name, self.name)

    def get_type(self):
        return self.type_name

    def get_name(self):
        return self.name

class cpp_func:
    def __init__(self,return_type,name):
        self.return_type = return_type
        self.name = name
        self.args = []

    def add_arg(self,arg):
        self.args.append(arg)

    def as_def_str(self):
        args_str = ""
        count = 0
        for arg in self.args:
            if count > 0:
                args_str += ", "
            args_str += arg.as_arg_str()
            count += 1

        return "{} {}({});\n".format(self.return_type,self.name,args_str)


class cpp_class:
    def __init__(self,name,parent = ""):
        self.name = name
        self.parent_class = parent
        self.vars = []
        self.methods = []

    def set_name(self,name):
        self.name = name

    def set_parent(self,parent):
        self.parent_class = parent

    def get_name(self):
        return self.name
    
    def get_parent(self):
        return self.parent_class

    def add_var(self,var,gen_get,gen_set):
        self.vars.append((var,gen_get,gen_set))

    def add_method(self,func):
        self.methods.append(func)

    def get_var_by_id(self,id):
        return self.vars[id]

    def get_method_by_id(self,id):
        return self.methods[id]

    def get_var_count(self):
        return len(self.vars)

    def get_method_count(self):
        return len(self.methods)

    def get_vars(self):
        return self.vars

    def get_methods(self):
        return self.methods

    def as_header_str(self):
        tab = "    "
        header = ""+"#ifndef {guard}_HPP\n"+"#define {guard}_HPP\n"+"\n"+"class {name} {inherit_statement}{{\n"+"    public:\n"+"{methods}\n"+"    private:\n"+"{variables}\n"+"}};\n"+"\n"+"#endif\n"
        comps = {}
        comps["guard"] = self.name.upper()
        print(comps["guard"])
        comps["inherit_statement"] = ""
        if self.parent_class != "":
            comps["inherit_statement"] = "public {} ".format(self.parent_class)

        comps["variables"] = ""
        getsetters = []
        for var in self.vars:
            comps["variables"] += tab + var[0].as_def_str()
            var_name = var[0].get_name()
            var_name = var_name.capitalize()
            if var[1]:
                getter = cpp_func(var[0].get_type(),"get"+var_name)
                getsetters.append(getter)
            if var[2]:
                setter = cpp_func("void","set"+var_name)
                setter.add_arg(var[0])
                getsetters.append(setter)

        comps["methods"] = ""
        for method in self.methods:
            comps["methods"] += tab + method.as_def_str()

        for getsetter in getsetters:
            comps["methods"] += tab + getsetter.as_def_str()

        print(comps)
        return header.format(guard=comps["guard"],name=self.name,inherit_statement=comps["inherit_statement"],methods=comps["methods"],variables=comps["variables"])
    
    def as_source_str(self):
        tab = "    "
        todo_notice = "//TODO implement"
        get_implement = "return {var_name}"
        set_implement = "this->{var_name} = {var_name}"
        method_template = "{return_type}{class_name}::{method_name}({method_params})\n{{\n"+tab+"{implement}\n}}\n\n"
        source = "#include \"{class_name}.hpp\"\n\n"+"{method_implementations}"

        method_implementations = ""
        for method in self.methods:
            return_type = ""
            if method.return_type != "":
                return_type = method.return_type + " "
            imp = todo_notice
            params = ""
            count = 0
            for param in method.args:
                if count != 0:
                    params += " ,"
                params += param.type_name + " " + param.name

            method_implementations += method_template.format(return_type=return_type,class_name=self.name,method_name=method.name,method_params=params,implement=imp)


        getters = []
        setters = []
        for var in self.vars:
            var_name = var[0].get_name()
            var_name = var_name.capitalize()
            if var[1]:
                getter = cpp_func(var[0].get_type()+" ","get"+var_name)
                get_imp = get_implement.format(var_name=var[0].get_name())
                method_implementations += method_template.format(return_type=getter.return_type,class_name=self.name,method_name=getter.name,method_params="",implement=get_imp)
            if var[2]:
                setter = cpp_func("void ","set"+var_name)
                setter.add_arg(var[0])
                set_imp = set_implement.format(var_name=var[0].get_name())
                parameters = var[0].type_name + " " + var[0].name
                method_implementations += method_template.format(return_type=setter.return_type,class_name=self.name,method_name=setter.name,method_params=parameters,implement=set_imp)            
            
        
        return source.format(class_name=self.name,method_implementations=method_implementations)


if __name__ == "__main__":
    foo = cpp_class("Foo","")
    var = cpp_var("int","a")
    arg = cpp_var("int","arg")
    func = cpp_func("int","add")
    func.add_arg(arg)
    foo.add_method(func)
    foo.add_var(var,True,True)

    print(foo.as_header_str())
    print(foo.as_source_str())
