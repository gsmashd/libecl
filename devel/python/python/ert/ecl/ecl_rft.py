#  Copyright (C) 2011  Statoil ASA, Norway. 
#   
#  The file 'ecl_rft.py' is part of ERT - Ensemble based Reservoir Tool. 
#   
#  ERT is free software: you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version. 
#   
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY 
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#  FITNESS FOR A PARTICULAR PURPOSE.   
#   
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html> 
#  for more details. 
"""
Module for loading ECLIPSE RFT files.
"""

import types
import warnings
from ert.cwrap import BaseCClass
from ert.ecl import EclRFTCell, EclPLTCell, EclPrototype
from ert.util import CTime

class EclRFT(BaseCClass):
    """The EclRFT class contains the information for *one* RFT.

    The ECLIPSE RFT file can contain three different types of RFT like
    objects which are lumped together; the EclRFTClass is a container
    for such objects. The three different object types which can be
    found in an RFT file are:
   
       RFT: This is old-fashioned RFT which contains measurements of
            saturations for each of the completed cells.
       
       PLT: This contains production and flow rates for each phase in
            each cell.

       SEGMENT: Not implemented.

    In addition to the measurements specific for RFT and PLT each cell
    has coordinates, pressure and depth.
    """
    TYPE_NAME = "ecl_rft"
    _alloc            = EclPrototype("void* ecl_rft_node_alloc_new( char* , char* , time_t , double)" , bind = False)
    _free             = EclPrototype("void  ecl_rft_node_free( ecl_rft )")
    _get_type         = EclPrototype("int    ecl_rft_node_get_type( ecl_rft )")
    _get_well         = EclPrototype("char*  ecl_rft_node_get_well_name( ecl_rft )")
    _get_date         = EclPrototype("time_t ecl_rft_node_get_date( ecl_rft )")
    _get_size         = EclPrototype("int ecl_rft_node_get_size( ecl_rft )")
    _iget_cell        = EclPrototype("void* ecl_rft_node_iget_cell( ecl_rft )")
    _iget_cell_sorted = EclPrototype("void* ecl_rft_node_iget_cell_sorted( ecl_rft )")
    _sort_cells       = EclPrototype("void* ecl_rft_node_inplace_sort_cells( ecl_rft )")
    _iget_depth       = EclPrototype("double ecl_rft_node_iget_depth( ecl_rft )")
    _iget_pressure    = EclPrototype("double ecl_rft_node_iget_pressure(ecl_rft)")
    _iget_ijk         = EclPrototype("void ecl_rft_node_iget_ijk( ecl_rft , int , int*, int*, int*)") 
    _iget_swat        = EclPrototype("double ecl_rft_node_iget_swat(ecl_rft)")
    _iget_sgas        = EclPrototype("double ecl_rft_node_iget_sgas(ecl_rft)")
    _iget_orat        = EclPrototype("double ecl_rft_node_iget_orat(ecl_rft)")
    _iget_wrat        = EclPrototype("double ecl_rft_node_iget_wrat(ecl_rft)")
    _iget_grat        = EclPrototype("double ecl_rft_node_iget_grat(ecl_rft)")
    _lookup_ijk       = EclPrototype("void* ecl_rft_node_lookup_ijk( ecl_rft , int , int , int)")
    _is_RFT           = EclPrototype("bool   ecl_rft_node_is_RFT( ecl_rft )")
    _is_PLT           = EclPrototype("bool   ecl_rft_node_is_PLT( ecl_rft )")
    _is_SEGMENT       = EclPrototype("bool   ecl_rft_node_is_SEGMENT( ecl_rft )")
    _is_MSW           = EclPrototype("bool   ecl_rft_node_is_MSW( ecl_rft )")


    def __init__(self , name , type_string , date , days):
        c_ptr = self._alloc( name , type_string , CTime( date ) , days )
        super(EclRFT , self).__init__( c_ptr )


    def free(self):
        self._free( )
    
    def __len__(self):
        """
        The number of completed cells in this RFT.
        """
        return self._get_size( )

    def is_RFT(self):
        """
        Is instance an RFT; in that case all the cells will be EclRFTCell instances.
        """
        return self._is_RFT( )

    def is_PLT(self):
        """
        Is instance a PLT; in that case all the cells will be EclPLTCell instances.
        """
        return self._is_PLT( )

    def is_SEGMENT(self):
        """
        Is this a SEGMENT - not implemented.
        """
        return self._is_SEGMENT( )

    def is_MSW(self):
        """
        Is this well a MSW well. Observe that the test ONLY applies to PLTs.
        """
        return self._is_MSW( )


    @property
    def type(self):
        # Enum: ecl_rft_enum from ecl_rft_node.h
        # RFT     = 1
        # PLT     = 2
        # Segment = 3  -- Not properly implemented
        """
        Deprecated - use query methods: is_RFT(), is_PLT() and is_SEGMENT() instead.
        """
        warnings.warn("The property type is deprecated, use the query methods is_RFT(), is_PLT() and is_SEGMENT() instead." , DeprecationWarning)
        return self._get_type( )


    def getWellName(self):
        """
        The name of the well we are considering.
        """
        return self._get_well( )
    
    @property
    def well(self):
        warnings.warn("The property well is deprecated, use the getWellName() method instead." , DeprecationWarning)
        return self.getWellName( )
        

    def getDate(self):
        """
        The date when this RFT/PLT/... was recorded. 
        """
        ct = CTime(self._get_date( ))
        return ct.date()

    
    @property
    def date(self):
        warnings.warn("The property date is deprecated, use the getDate() instead." , DeprecationWarning)
        return self.getDate()
    
        
    @property
    def size(self):
        """
        The number of completed cells.
        """
        warnings.warn("The property size is deprecated, use the built in len( ) function instead." , DeprecationWarning)
        return len(self)


    def __cell_ref( self , cell_ptr ):
        if self.is_RFT():
            return EclRFTCell.createCReference( cell_ptr , self )
        elif self.is_PLT():
            return EclPLTCell.createCReference( cell_ptr , self )
        else:
            raise NotImplementedError("Only RFT and PLT cells are implemented")


    def assert_cell_index( self , index ):
        if isinstance( index , types.IntType):
            length = self.__len__()
            if index < 0 or index >= length:
                raise IndexError
        else:
            raise TypeError("Index should be integer type")


    def __getitem__(self , index):
        """Implements the [] operator to return the cells.

        To get the object related to cell nr 5:

           cell = rft[4]

        The return value from the __getitem__() method is either an
        EclRFTCell instance or a EclPLTCell instance, depending on the
        type of this particular RFT object. 
        """
        self.assert_cell_index( index )
        cell_ptr = self._iget_cell( index )
        return self.__cell_ref( cell_ptr )
        

    def iget( self , index ):
        return self[index]

        
    def iget_sorted( self , index ):
        """
        Will return the cell nr @index in the list of sorted cells. 

        See method sort() for further documentation.
        """
        self.assert_cell_index( index )
        cell_ptr = self._iget_cell_sorted( index )
        return self.__cell_ref( cell_ptr )
        

    def sort(self):
        """
        Will sort cells in RFT; currently only applies to MSW wells.

        By default the cells in the RFT come in the order they are
        specified in the ECLIPSE input file; that is not necessarily
        in a suitable order. In the case of MSW wells it is possible
        to sort the connections after distance along the wellpath. To
        access the cells in sort order you have two options:

           1. Sort the cells using the sort() method, and then
              subsequently access them sequentially:

                rft.sort()
                for cell in rft:
                    print cell

           2. Let the rft object stay unsorted, but access the cells
              using the iget_sorted() method:

                 for i in range(len(rft)):
                     cell = rft.iget_sorted( i )
        
        Currently only MSW/PLTs are sorted, based on the CONLENST
        keyword; for other wells the sort() method does nothing.  
        """
        self._sort_cells( )


    # ijk are zero offset
    def ijkget( self , ijk ):
        """
        Will look up the cell based on (i,j,k).

        If the cell (i,j,k) is not part of this RFT/PLT None will be
        returned. The (i,j,k) input values should be zero offset,
        i.e. you must subtract 1 from the (i,j,k) values given in the ECLIPSE input.
        """
        cell_ptr = self._lookup_ijk( ijk[0] , ijk[1] , ijk[2])
        if cell_ptr:
            return self.__cell_ref( cell_ptr )
        else:
            return None




class EclRFTFile(BaseCClass):
    TYPE_NAME = "ecl_rft_file"
    _load          = EclPrototype("void* ecl_rft_file_alloc_case( char* )", bind = False)
    _iget          = EclPrototype("ecl_rft_ref ecl_rft_file_iget_node( ecl_rft_file , int )")
    _get_rft       = EclPrototype("ecl_rft_ref ecl_rft_file_get_well_time_rft( ecl_rft_file , char* , time_t)")
    _has_rft       = EclPrototype("bool ecl_rft_file_case_has_rft( char* )", bind = False)
    _free          = EclPrototype("void ecl_rft_file_free( ecl_rft_file )")
    _get_size      = EclPrototype("int ecl_rft_file_get_size__( ecl_rft_file , char* , time_t)")
    _get_num_wells = EclPrototype("int  ecl_rft_file_get_num_wells( ecl_rft_file )")


    """
    The EclRFTFile class is used to load an ECLIPSE RFT file.

    The EclRFTFile serves as a container which can load and hold the
    content of an ECLIPSE RFT file. The RFT files will in general
    contain data for several wells and several times in one large
    container. The EclRFTClass class contains methods get the the RFT
    results for a specific time and/or well. 

    The EclRFTFile class can in general contain a mix of RFT and PLT
    measurements. The class does not really differentiate between
    these.
    """

    def __init__(self , case):
        c_ptr = self._load( case )
        super(EclRFTFile , self).__init__(c_ptr)


    def __len__(self):
        return self._get_size(  None , CTime(-1))


    def __getitem__(self, index):
        if isinstance(index, int):
            if 0 <= index < len(self):
                rft = self._iget(index)
                rft.setParent( self )
                return rft
            else:
                raise IndexError("Index '%d' must be in range: [0, %d]" % (index, len(self) - 1))
        else:
            raise TypeError("Index must be integer type")

    
    def size(self, well=None, date=None):
        """
        The number of elements in EclRFTFile container. 

        By default the size() method will return the total number of
        RFTs/PLTs in the container, but by specifying the optional
        arguments date and/or well the function will only count the
        number of well measurements matching that time or well
        name. The well argument can contain wildcards.

           rftFile = ecl.EclRFTFile( "ECLIPSE.RFT" )
           print "Total number of RFTs : %d" % rftFile.size( )
           print "RFTs matching OP*    : %d" % rftFile.size( well = "OP*" )
           print "RFTs at 01/01/2010   : %d" % rftFile.size( date = datetime.date( 2010 , 1 , 1 ))

        """
        if date:
            cdate = CTime( date )
        else:
            cdate = CTime( -1 )

        return self._get_size( well , cdate)


    def getNumWells(self):
        """
        Returns the total number of distinct wells in the RFT file.
        """
        return self._get_num_wells( )
        
    @property
    def num_wells( self ):
        warnings.warn("The property num_wells is deprecated, use the getNumWells() instead." , DeprecationWarning)
        return self.getNumWells()

    
    def getHeaders(self):
        """
        Returns a list of two tuples (well_name , date) for the whole file.
        """
        header_list = []
        for i in (range(self._get_size( None , CTime(-1)))):
            rft = self.iget( i )
            header_list.append( (rft.well , rft.date) )
        return header_list

    @property
    def headers(self):
        warnings.warn("The property headers is deprecated, use the getHeaders() instead." , DeprecationWarning)
        return self.getHeaders()
    

    def iget(self , index):
        """
        Will lookup RFT @index - equivalent to [@index].
        """
        return self[index]


    def get(self , well_name , date ):
        """
        Will look up the RFT object corresponding to @well and @date.

        Raise Exception if not found.
        """
        if self.size( well = well_name , date = date) == 0:
            raise KeyError("No RFT for well:%s at %s" % (well_name , date))

        rft = self._get_rft( well_name , CTime( date )) 
        rft.setParent( self )
        return rft

    def free(self):
        self._free( )
    









