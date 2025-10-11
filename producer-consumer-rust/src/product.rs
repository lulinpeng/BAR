use std::fmt;

#[derive(Debug)]
pub struct Product {
    id: u32,
    name: String,
}

impl Product {
    pub fn new(id: u32, name: &str) -> Self {
        Product {
            id,
            name: name.to_string(),
        }
    }
}

impl fmt::Display for Product {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "ID: {}, Name: {}", self.id, self.name,)
    }
}
