import React from "react";
import { Typography, Grid, TextField, FormHelperText, FormControl } from '@material-ui/core'
import { AccountCircle } from '@material-ui/icons';

const LiveTextField = (props) => {

    const handleFieldChange = e => {
        // change the value of field when the text is changing
        props.changeField(e, props.fieldName);
    }

    return (
        <>
            <Grid item xs={12} spacing={3} align='center'>
                {props.icon}
            {/* </Grid>
            <Grid item xs={12} spacing={0} align='center'> */}
                <FormControl> 
                        <TextField
                            variant="outlined"
                            label={props.fieldName}
                            // {props.fieldName}
                            // value={props.field}
                            onChange={handleFieldChange}
                            
                        />
                
                        <FormHelperText>
                            {props.helperText}
                        </FormHelperText>
                    </FormControl>
            </Grid>
        </>
    );
};

export default LiveTextField;