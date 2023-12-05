// Header.js
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { updatePageType } from '../redux/textSlice';

function Header() {
  const dispatch = useDispatch();

  const handleNavClick = (pageType) => {
    dispatch(updatePageType(pageType));
  };

  const pageType = useSelector((state) => state.text.pageType);

  let dropdownTitle;
  switch (pageType) {
    case 'c1':
      dropdownTitle = 'C1: Fully-Automatic';
      break;
    case 'c2':
      dropdownTitle = 'C2: Mixed-Initiative';
      break;
    default:
      dropdownTitle = null;
      break;
  }

  return (
    <Navbar expand="lg">
      <Navbar.Brand href="#" onClick={() => handleNavClick('c0')}>VL2NL Prototype</Navbar.Brand>
      <Nav className="justify-content-end flex-grow-1">
        <NavDropdown title={dropdownTitle} id="collapsible-nav-dropdown">
          <NavDropdown.Item onClick={() => handleNavClick('c1')}>C1: Fully-Automatic</NavDropdown.Item>
          <NavDropdown.Divider />
          <NavDropdown.Item onClick={() => handleNavClick('c2')}>C2: Mixed-Initiative</NavDropdown.Item>
        </NavDropdown>
      </Nav >
    </Navbar >
  )
}

export default Header;
