from app import db
from flask_login import UserMixin

# ============================
# MANY-TO-MANY: Hairstyles ↔ Hair Attachments
# ============================

HairStyle_HairAttachments = db.Table(
    'hairStyle_hairAttachments',
    db.Column('hair_style_id', db.Integer, db.ForeignKey('hair_styles.id'), primary_key=True),
    db.Column('hair_attachment_id', db.Integer, db.ForeignKey('hair_attachments.id'), primary_key=True)
)

# ============================
# SERVICE PROVIDER ↔ HAIRSTYLE (with duration)
# ============================

class ServiceProviderHairstyle(db.Model):
    __tablename__ = 'service_provider_hairstyles'
    __table_args__ = (
    db.UniqueConstraint('service_provider_id', 'hair_style_id'),
    )


    id = db.Column(db.Integer, primary_key=True)
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    hair_style_id = db.Column(db.Integer, db.ForeignKey('hair_styles.id'), nullable=False)

    duration_minutes = db.Column(db.Integer, nullable=False)

    service_provider = db.relationship("ServiceProvider", back_populates="hairstyle_associations")
    hairstyle = db.relationship("HairStyle", back_populates="service_provider_associations")

    def __repr__(self):
        return f"<SP_Hairstyle (SP:{self.service_provider_id}, HS:{self.hair_style_id}, {self.duration_minutes}m)>"

    def to_dict(self):
        return {
            "id": self.id,
            "service_provider_id": self.service_provider_id,
            "hair_style_id": self.hair_style_id,
            "duration_minutes": self.duration_minutes
        }

# ============================
# SERVICE PROVIDER ↔ SERVICES (price, duration, image)
# ============================

class ServiceProviderServices(db.Model):
    __tablename__ = 'service_provider_services'

    id = db.Column(db.Integer, primary_key=True)
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    price = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(100), nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=False)

    service_provider = db.relationship("ServiceProvider", back_populates="service_associations")
    service = db.relationship("Service", back_populates="service_provider_associations")

    def to_dict(self):
        return {
            "id": self.id,
            "service_provider_id": self.service_provider_id,
            "service_id": self.service_id,
            "price": self.price,
            "picture": self.picture,
            "duration_minutes": self.duration_minutes
        }

# ============================
# HAIR STYLES
# ============================

class HairStyle(db.Model):
    __tablename__ = 'hair_styles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=False)

    attachments = db.relationship(
        'HairAttachment',
        secondary=HairStyle_HairAttachments,
        lazy='subquery',
        backref=db.backref('hair_styles', lazy=True)
    )

    service_provider_associations = db.relationship(
        "ServiceProviderHairstyle",
        back_populates="hairstyle"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "category": self.category,
            "attachments": [a.to_dict() for a in self.attachments]
        }

# ============================
# HAIRSTYLE ALIASES
# ============================

class HairStyleAlias(db.Model):
    __tablename__ = 'hair_style_aliases'

    id = db.Column(db.Integer, primary_key=True)
    service_provider_hairstyle_id = db.Column(
        db.Integer, db.ForeignKey('service_provider_hairstyles.id'), nullable=False
    )
    alias_name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "alias_name": self.alias_name,
            "service_provider_hairstyle_id": self.service_provider_hairstyle_id
        }

# ============================
# HAIR ATTACHMENTS
# ============================

class HairAttachment(db.Model):
    __tablename__ = 'hair_attachments'

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    texture = db.Column(db.String(100), nullable=False)
    length = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "picture": self.picture,
            "name": self.name,
            "color": self.color,
            "texture": self.texture,
            "length": self.length,
            "brand": self.brand,
            "price": self.price,
            "type": self.type,
            "description": self.description
        }

# ============================
# SERVICES
# ============================

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    service_provider_associations = db.relationship(
        'ServiceProviderServices',
        back_populates='service'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

# ============================
# SERVICE PROVIDERS
# ============================

class ServiceProvider(db.Model):
    __tablename__ = 'service_providers'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False, default='service_provider')
    surname = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    id_card_number = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(100), nullable=True)
    about = db.Column(db.Text)
    password = db.Column(db.String(200), nullable=False)


    def is_service_provider(self):
        return self.role == "service_provider"

    reviews = db.relationship("Review", backref="service_provider", lazy="joined")
    appointments = db.relationship("Appointment", backref="service_provider", lazy=True)

    hairstyle_associations = db.relationship(
        "ServiceProviderHairstyle",
        back_populates="service_provider"
    )

    service_associations = db.relationship(
        'ServiceProviderServices',
        back_populates='service_provider'
    )
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "surname": self.surname,
            "given_name": self.given_name,
            "id_card_number": self.id_card_number,
            "phone_number": self.phone_number,
            "location": self.location,
            "about": self.about,
            "hairstyle_associations": [a.id for a in self.hairstyle_associations],
            "services": [s.id for s in self.service_associations],
            "appointments": [a.id for a in self.appointments],
            "reviews": [r.id for r in self.reviews],
        }

# ============================
# CLIENTS
# ============================

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=False)
    role = db.Column(db.String(100), nullable=False, default='client')
    picture = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.Text, nullable=False)
    hair_type = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    
    reviews = db.relationship("Review", backref="client", lazy=True)
    appointments = db.relationship("Appointment", backref="client", lazy=True)
    
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def is_client(self):
        return self.role == "client"

    def to_dict(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "given_name": self.given_name,
            "email": self.email,
            "contact_info": self.phone_number,
            "location": self.location,
            "hair_type": self.hair_type,
            "role": self.role
        }

# ============================
# REVIEWS
# ============================

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)

    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "client_id": self.client_id,
            "rating": self.rating,
            "service_provider_id": self.service_provider_id
        }

# ============================
# APPOINTMENTS
# ============================

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    venue = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(100), nullable=False, default='pending')

    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    hair_style_id = db.Column(db.Integer, db.ForeignKey('hair_styles.id'))
    hair_style = db.relationship("HairStyle")

    def to_dict(self):
        return {
            "id": self.id,
            "service_provider_id": self.service_provider_id,
            "client_id": self.client_id,
            "date_created": self.date_created,
            "appointment_time": self.appointment_time,
            "venue": self.venue,
            "price": self.price,
            "duration": self.duration,
            "status": self.status,
            "hair_style": self.hair_style
        }


# ============================
# SERVICE ALIASES
# ============================

class ServiceAlias(db.Model):
    __tablename__ = 'service_aliases'

    id = db.Column(db.Integer, primary_key=True)
    alias_name = db.Column(db.String(100), nullable=False)
    service_provider_services_id = db.Column(
        db.Integer, db.ForeignKey('service_provider_services.id'), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "alias_name": self.alias_name,
            "service_provider_services_id": self.service_provider_services_id
        }
