import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import UsersList from '../UsersList';

const users = [
    {
        'active': true,
        'email': 'kevinmogollon@upeu.edu.pe',
        'id': 1,
        'username': 'kevin'
    },
    {
        'active': true,
        'email': 'abelthf@gmail.com',
        'id': 2,
        'username': 'fredy'
    }
];

test('UsersList renders properly', () =>{
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('kevin');
});     

test('UsersList renders a snapshot', () =>{
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});
