import React, { useState, useEffect } from "react";
import { Typography, Grid, withStyles, Card, CardContent, Container } from '@material-ui/core'
import InputTextField from '../components/InputTextField';
import LiveTextField from '../components/LiveTextField';
import SmallButton from '../components/SmallButton';
import { Add, Search, SkipPreviousRounded } from '@material-ui/icons'
import ResultStrings from '../components/ResultStrings';


const textFieldInfo = [
    {
        fieldName: 'Repo Name',
        icon: <Add style={{color: '#7b113a'}}/>,
        helperText: 'Add a repo'
    },
    {
        fieldName: 'Repo Name',
        icon: <Search style={{color: '#7b113a'}}/>,
        helperText: 'Search for repo'
    }
]

const rows = [
    {
        id: 1,
        repoName: 'Repo 1',
        userName: 'Test 1'
    },
    {
        id: 2,
        repoName: 'Repo 2',
        userName: 'Test 2'
    },
    {
        id: 3,
        repoName: 'Repo 3',
        userName: 'Test 3'
    }, 
    {
        id: 1,
        repoName: 'Repo 1',
        userName: 'Test 1'
    },
    {
        id: 2,
        repoName: 'Repo 2',
        userName: 'Test 2'
    },
    {
        id: 3,
        repoName: 'Repo 3',
        userName: 'Test 3'
    }
];


const MainPage = () => {

    const BurgendyTextTypography = withStyles({
        root: {
          color: "#150e56"
        }
      })(Typography);

    // set the states of the fields
    const [fieldObj, setFieldObj] = useState({addUser: '', searchRepo: ''})

    const changeRepo = (e, field) => {
        // console.log(fieldObj)
        // change the value of add repo
        setFieldObj(prevState => {
            const currObj = {...prevState};
            currObj[field] = e.target.value;
            return currObj;
        })

        // send a request to the backend if search repo is being touched
        if (field === 'searchRepo') {
            console.log('Call endpoint to search repos for ' + fieldObj[field])
        }
    }

    const addUser = (e) => {
        // send post request to backend
        console.log(fieldObj['addUser']);

        // clear the user from the object
        setFieldObj(prevState => {
            const currObj = {...prevState};
            currObj['addUser'] = '';
            return currObj;
        })
    }

    useEffect(() => {
        console.log(fieldObj);
    });

    return (
        <>
        <Container maxWidth='xs'>
            <Grid container spacing={5} alignItems='center'>
                <Grid item xs={12} className='title' align='center'>
                    <BurgendyTextTypography variant='h2'> Beyond Search </BurgendyTextTypography>
                </Grid>
                
                <Grid item xs={12} align='center'>
                    <Card>
                        <CardContent>
                            <InputTextField fieldValue={fieldObj['addUser']} fieldName='User Name' icon={ <Add style={{color: '#7b113a'}} /> } helperText= 'Add a github user' updateTextField={changeRepo}/>
                            <SmallButton buttonClicked={addUser}/>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} align='center'>
                    <Card>
                            <CardContent>
                                <InputTextField fieldValue={fieldObj['searchRepo']} fieldName='Repo Name' icon={ <Search style={{color: '#7b113a'}} /> } helperText= 'Search for repo' updateTextField={changeRepo}/>
                            </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} align='center'>
                    <ResultStrings rows={rows}/>
                </Grid>
              
            </Grid>
            </Container>
        </>
    );
};

export default MainPage;