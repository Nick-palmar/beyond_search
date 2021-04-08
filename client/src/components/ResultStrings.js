import React from "react";
import { Table, TableContainer, TableHead, TableRow, TableCell, TableBody, withStyles } from '@material-ui/core'

const ResultStrings = (props) => {


    const StyledTableCell = withStyles({
        root: {
          color: '#150e56'
        }
      })(TableCell);

    return (
        <>
            <TableContainer>
                <Table aria-label="simple-table">
                    <TableHead> 
                        <TableRow> 
                            <StyledTableCell component="th" scope="row" >Id</StyledTableCell>
                            <StyledTableCell align="right">Repo Name</StyledTableCell>
                            <StyledTableCell align="right" >Github User</StyledTableCell>
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {props.rows.map(row => (    
                            <TableRow key={row.id}>
                                <StyledTableCell component="th" scope="row">
                                    {row.id}
                                </StyledTableCell>
                                <StyledTableCell align="right" >{row.repoName}</StyledTableCell>
                                <StyledTableCell align="right" >{row.userName}</StyledTableCell>
                            </TableRow>     
                         ))}

                    </TableBody>
                </Table>
            </TableContainer>
        </>
    );
};

export default ResultStrings;