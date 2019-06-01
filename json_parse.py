
from collections import deque

def str_to_base_obj(s: str, current_type):
    if s == 'null':
        return None, 'None'
    if s.isdigit() and current_type != 'string':
        return float(s), 'float'
    if s.isalpha() or current_type == 'string' or current_type == 'string_dict':
        return s, 'str'


def str_to_obj(s: str, curr_type=None):
    """function return correspond type of python object (type_obj) and list for iterable objects"""

    ket = (']', '}', '",', '\',')  # tuple of close brackets, which actually indicate end of
    # iterable object and it used for make "pop steck"

    if curr_type != 'string':  # if string we write any char to current string
        if s == '[':
            return [], 'list_open'

        elif s == '{':  # start to write keys at list that returned here
            return {}, 'dict_open'

        elif (s == '"') or (s == '\''):
            return '', 'string'

        else:
            return s, 'base_type'
    else:
        return s, 'base_type'




def update_stack(obj, type_obj, stack):

    if type_obj == 'pop':
        buffer = stack.pop()[0]
        curr_type = stack[-1][1]
        append_to_current_object(buffer, curr_type, stack)
        return curr_type
    if type_obj == 'pop_value':
        value = stack.pop()[0]
        key = stack.pop()[0]
        stack[-1][0][key] = value
    else:
        stack.append([obj, type_obj])
        return type_obj


def append_to_current_object(local_obj, curr_type, stack):

    if curr_type == 'list_open' or curr_type == 'stack_level':
        stack[-1][0].append(local_obj)

    if curr_type == 'string' or curr_type == 'key_open' or curr_type == 'value_open':
        stack[-1][0] = local_obj
        #может лучше тут закрывать стэк стрингов


def read_local_object(local_str, char, curr_type, reading_done=False, dict_open=False):

    if reading_done:
        local_str = ''



    if local_str != '' and (char == ',' or char == ']' or char == '}' or char == ':'):

        if curr_type == 'string' and (local_str[-1] == '\'' or local_str[-1] == '"'):
            return local_str[:-1], True

        if curr_type != 'string':
            return local_str, True


    return local_str + char, False




def parse_json(file_name: str):

    stack = deque([])
    stack.append([[], 'stack_level'])
    local_str = ''
    char = True
    reading_done = False
    stack_print = False
    i = 0
    with open(file_name, "r") as json_file:

        while bool(char):

            char = json_file.read(1)

            curr_type = stack[-1][1]
            obj, type_obj = str_to_obj(char, curr_type)

            if curr_type != 'string' and char == ' ':
                pass


            elif type_obj != 'base_type':
                curr_type = update_stack(obj, type_obj, stack) # можно возвращать сзесь каррент тип

            else:
                local_str, reading_done = read_local_object(local_str, char, curr_type, reading_done)

                if reading_done:
                    if local_str != '':
                        local_obj = str_to_base_obj(local_str.lstrip(), curr_type)[0]

                        if curr_type == 'string':
                            curr_type = update_stack(obj=None, type_obj='pop', stack=stack)

                        if curr_type == 'dict_open':
                            curr_type = update_stack(None, type_obj='key_open', stack=stack)

                        append_to_current_object(local_obj, curr_type, stack)

                    if curr_type == 'value_open':
                        curr_type = update_stack(None, type_obj='pop_value', stack=stack)


                    if char == ',' and curr_type == 'string':
                        curr_type = update_stack(obj=None, type_obj='pop', stack=stack)

                    if char == ']' or char == '}':
                        if curr_type == 'string':
                            curr_type = update_stack(obj=None, type_obj='pop', stack=stack)

                        curr_type = update_stack(obj=None, type_obj='pop', stack=stack)
                    if char == ':' and curr_type == 'key_open':
                        curr_type = update_stack(None, type_obj='value_open', stack=stack)



        print(stack[0])
        print(len(stack))



if __name__ == '__main__':
    #parse_json('test.json')


    parse_json("winedata_1.json")

