import logging
from re import search
from tkinter import Entry

logger = logging.getLogger('validation_controller')


def str_validate(action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name, lentgh: int=None) -> bool:
    '''
    str_validate
    ------------

    Args
        - action -> %d - Action code: 0 for deletion 1 for insertion
        - index -> %i - index of the insertion o deletion 
        - value_if_allowed -> %P - Text value in change is permited
        - prior_value -> %s - Text before the change
        - text -> %S -> Call due insertion or deletion, this will be the text being deleted or inserted
        - validation_type -> %v - Present value of the validade option of the widget
        - trigger_type -> %V - Callback due to one of the string values i.e: "focusin", "focusout", "key" or "forced"
        - widget_name -> %W - Name of the widget
        - lentgh -> custom var the max lenth allowed
    '''
    if(action=='1'):
        try:
            str(value_if_allowed)
            if not lentgh:
                return True
            if len(value_if_allowed) <= int(lentgh):
                return True
            return False
        except ValueError:
            return False
    else:
        return True

def int_validate(action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name, lentgh: int=None):
    '''
    int_validate
    ------------
    
    Args
        - action -> %d - Action code: 0 for deletion 1 for insertion
        - index -> %i - index of the insertion o deletion 
        - value_if_allowed -> %P - Text value in change is permited
        - prior_value -> %s - Text before the change
        - text -> %S -> Call due insertion or deletion, this will be the text being deleted or inserted
        - validation_type -> %v - Present value of the validade option of the widget
        - trigger_type -> %V - Callback due to one of the string values i.e: "focusin", "focusout", "key" or "forced"
        - widget_name -> %W - Name of the widget
        - lentgh -> custom var the max lenth allowed
    '''    
    # action=1 -> insert
    if(action=='1'):
        if search('[0-9]+', text) or text in '0123456789':
            try:
                int(value_if_allowed)
                if not lentgh:
                    return True
                if len(value_if_allowed) <= int(lentgh):
                    return True
                return False
            except ValueError:
                return False
        else:
            return False
    else:
        return True


def float_validate(action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name):
    '''
    float_validate
    --------------

    Args
        - action -> %d - Action code: 0 for deletion 1 for insertion
        - index -> %i - index of the insertion o deletion 
        - value_if_allowed -> %P - Text value in change is permited
        - prior_value -> %s - Text before the change
        - text -> %S -> Call due insertion or deletion, this will be the text being deleted or inserted
        - validation_type -> %v - Present value of the validade option of the widget
        - trigger_type -> %V - Callback due to one of the string values i.e: "focusin", "focusout", "key" or "forced"
        - widget_name -> %W - Name of the widget
    '''    
    # action=1 -> insert
    if (action=='1'):
        if search('[+-]?[0-9]+[\.\,]?[0-9]+', text) or text in '0123456789,.-+':
            try:
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True    


def bool_validate(action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name):
    '''
    float_validate
    --------------

    Args
        - action -> %d - Action code: 0 for deletion 1 for insertion
        - index -> %i - index of the insertion o deletion 
        - value_if_allowed -> %P - Text value in change is permited
        - prior_value -> %s - Text before the change
        - text -> %S -> Call due insertion or deletion, this will be the text being deleted or inserted
        - validation_type -> %v - Present value of the validade option of the widget
        - trigger_type -> %V - Callback due to one of the string values i.e: "focusin", "focusout", "key" or "forced"
        - widget_name -> %W - Name of the widget
    '''    
    # action=1 -> insert
    if action:
        return True
    else:
        return False


def entry_format(entry: Entry, type: object, type_format: str=None) -> str:
    '''
    entry_format
    ------------

    '''
    entry_value = entry.get()
    if entry_value:
        entry_value = entry_value.strip()
        if type == float:
            entry_value = entry_value.replace(',', '.')
            if len(entry_value) == 1 and entry_value in '-+':
                return entry_value
        type_value = type(entry_value)
        if type_format:
            insert_value = f'{type_value:{type_format}}'
        else:
            insert_value = type_value
        entry.delete(0, 'end')
        entry.insert(0, insert_value)
        return insert_value
    return None
            

def value_format(value: str, type: object, type_format: str=None) -> str | None:
    if value:
        try:
            value = value.strip()
            if type == float:
                value = value.replace(',', '.')
            value_in_type = type(value)
            if type_format:
                return f'{value_in_type:{type_format}}'
            else:
                return value_in_type
        except ValueError:
            return None

def strike_str(text: any) -> str:
    text = str(text)
    return ' ' + '\u0336'.join(text).strip()

def remove_strike(text: str) -> str:
    return text.replace('\u0336', '')