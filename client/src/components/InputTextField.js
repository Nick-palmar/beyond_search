import React from "react";
import { Typography, Grid, TextField, FormHelperText, FormControl } from '@material-ui/core'
import { AccountCircle } from '@material-ui/icons';

const InputTextField = (props) => {

    const handleFieldChange = e => {
        // change the value of field when the text is changing
        if (props.helperText === 'Add a github user') {
            props.updateTextField(e, 'addUser');
        }
        else {
            // assume the only other case is search repo
            props.updateTextField(e, 'searchRepo')
        }
    }

    return (
        <>
            <Grid item xs={12} align='center'>
                {props.icon}
            {/* </Grid>
            <Grid item xs={12} spacing={0} align='center'> */}
                <FormControl> 
                        <TextField
                            variant="outlined"
                            label={props.fieldName}
                            // {props.fieldName}
                            value={props.fieldValue}
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

export default InputTextField;