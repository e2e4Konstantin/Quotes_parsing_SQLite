from collections import namedtuple

# DataFile(name='c:\\tmp\\WORK_PROCESS_67.xlsx', period=67)
DataFile = namedtuple(typename='DataFile', field_names=['name', 'period'])
DataFile.__annotations__ = {'name': str, 'period': int}


SrcData = namedtuple(typename='SrcData', field_names=['catalog', 'quote', 'statistics'], defaults=(None, None, ""))
SrcData.__annotations__ = {'catalog': list[DataFile], 'quote': list[DataFile], 'statistics': str}


SrcMachinesData = namedtuple(typename='SrcMachinesData',
                             field_names=['path', 'structure', 'machines'],
                             defaults=("", "", ""))
SrcData.__annotations__ = {'path': str, 'structure': str, 'machines': str}

