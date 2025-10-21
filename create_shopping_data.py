#!/usr/bin/env python
"""
GLI-L 코인 쇼핑몰 초기 데이터 생성 스크립트

3개 카테고리:
1. 리조트&호텔 예약 (resort)
2. 상품 (goods)
3. 레스토랑 (restaurant)
"""
import os
import django
from decimal import Decimal

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gli_content.models import ShoppingCategory, ShoppingProduct


def create_categories():
    """카테고리 생성"""
    categories_data = [
        {
            'name': '리조트&호텔 예약',
            'name_en': 'Resort & Hotel Booking',
            'description': 'GLI-L 토큰으로 예약할 수 있는 프리미엄 리조트와 호텔',
            'description_en': 'Premium resorts and hotels that can be booked with GLI-L tokens',
            'icon': '🏨',
            'order': 1,
        },
        {
            'name': '상품',
            'name_en': 'Products',
            'description': 'GLI-L 토큰으로 구매할 수 있는 프리미엄 상품들',
            'description_en': 'Premium products that can be purchased with GLI-L tokens',
            'icon': '🛍️',
            'order': 2,
        },
        {
            'name': '레스토랑',
            'name_en': 'Restaurant',
            'description': 'GLI-L 토큰으로 예약할 수 있는 파인 다이닝 레스토랑',
            'description_en': 'Fine dining restaurants that can be booked with GLI-L tokens',
            'icon': '🍽️',
            'order': 3,
        },
    ]

    categories = {}
    for data in categories_data:
        category, created = ShoppingCategory.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✅ 카테고리 생성: {category.name}")
        else:
            print(f"⏭️  카테고리 존재: {category.name}")
        categories[category.name_en.split()[0].lower()] = category

    return categories


def create_resort_products(category):
    """리조트 & 호텔 상품 생성"""
    resorts_data = [
        {
            'name': 'GLI Ocean Resort',
            'name_en': 'GLI Ocean Resort',
            'description': '제주도의 아름다운 해변가에 위치한 럭셔리 리조트입니다. 전 객실에서 오션뷰를 즐길 수 있으며, 최고급 편의시설을 갖추고 있습니다.',
            'description_en': 'A luxury resort located on the beautiful beachfront of Jeju Island. All rooms offer ocean views and are equipped with premium amenities.',
            'short_description': '제주도 오션뷰 럭셔리 리조트',
            'short_description_en': 'Jeju Island Ocean View Luxury Resort',
            'product_type': 'resort',
            'price_glil': Decimal('150.00'),
            'price_usd': Decimal('150.00'),
            'stock_quantity': 50,
            'main_image_url': 'https://placehold.co/800x600/1E90FF/FFFFFF/png?text=GLI+Ocean+Resort',
            'is_featured': True,
            'tags': ['오션뷰', '럭셔리', '제주도', '5성급', 'Ocean View', 'Luxury', 'Jeju', '5-Star'],
            'attributes': {
                'location': 'Jeju Island, Korea',
                'location_en': 'Jeju Island, Korea',
                'rating': 5,
                'rooms': [
                    {
                        'type': 'standard',
                        'type_ko': '스탠다드',
                        'price': 150,
                        'features': ['Ocean View', 'Free WiFi', 'Breakfast Included'],
                        'features_ko': ['오션뷰', '무료 WiFi', '조식 포함']
                    },
                    {
                        'type': 'deluxe',
                        'type_ko': '디럭스',
                        'price': 250,
                        'features': ['Premium Ocean View', 'Balcony', 'Room Service', 'Mini Bar'],
                        'features_ko': ['프리미엄 오션뷰', '발코니', '룸서비스', '미니바']
                    },
                    {
                        'type': 'suite',
                        'type_ko': '스위트',
                        'price': 450,
                        'features': ['Panoramic View', 'Separate Living Room', 'Jacuzzi', 'Butler Service'],
                        'features_ko': ['파노라믹 뷰', '별도 거실', '자쿠지', '버틀러 서비스']
                    }
                ]
            },
        },
        {
            'name': 'GLI Mountain Lodge',
            'name_en': 'GLI Mountain Lodge',
            'description': '설악산의 청정 자연 속에서 힐링할 수 있는 마운틴 리조트입니다. 사계절 아름다운 경관과 함께 다양한 액티비티를 즐길 수 있습니다.',
            'description_en': 'A mountain resort where you can heal in the pristine nature of Seoraksan. Enjoy various activities with beautiful scenery in all four seasons.',
            'short_description': '설악산 자연 속 힐링 리조트',
            'short_description_en': 'Healing Resort in Seoraksan Nature',
            'product_type': 'resort',
            'price_glil': Decimal('120.00'),
            'price_usd': Decimal('120.00'),
            'stock_quantity': 40,
            'main_image_url': 'https://placehold.co/800x600/228B22/FFFFFF/png?text=GLI+Mountain+Lodge',
            'is_featured': True,
            'tags': ['산악', '자연', '설악산', '힐링', 'Mountain', 'Nature', 'Seoraksan', 'Healing'],
            'attributes': {
                'location': 'Gangwon-do, Korea',
                'location_en': 'Gangwon-do, Korea',
                'rating': 4,
                'rooms': [
                    {
                        'type': 'standard',
                        'type_ko': '스탠다드',
                        'price': 120,
                        'features': ['Mountain View', 'Heating', 'Free Parking'],
                        'features_ko': ['마운틴 뷰', '난방', '무료 주차']
                    },
                    {
                        'type': 'deluxe',
                        'type_ko': '디럭스',
                        'price': 200,
                        'features': ['Premium Mountain View', 'Fireplace', 'Private Deck'],
                        'features_ko': ['프리미엄 마운틴 뷰', '벽난로', '프라이빗 데크']
                    },
                    {
                        'type': 'villa',
                        'type_ko': '빌라',
                        'price': 380,
                        'features': ['Private Villa', 'Hot Tub', 'Kitchen', 'BBQ Area'],
                        'features_ko': ['프라이빗 빌라', '온수 욕조', '주방', 'BBQ 공간']
                    }
                ]
            },
        },
        {
            'name': 'GLI City Hotel',
            'name_en': 'GLI City Hotel',
            'description': '서울 도심 속 비즈니스와 레저를 동시에 즐길 수 있는 프리미엄 호텔입니다. 최신 시설과 편리한 교통으로 완벽한 서울 여행을 경험하세요.',
            'description_en': 'A premium hotel in the heart of Seoul where you can enjoy both business and leisure. Experience the perfect Seoul trip with modern facilities and convenient transportation.',
            'short_description': '서울 도심 프리미엄 호텔',
            'short_description_en': 'Seoul Premium City Hotel',
            'product_type': 'resort',
            'price_glil': Decimal('180.00'),
            'price_usd': Decimal('180.00'),
            'stock_quantity': 60,
            'main_image_url': 'https://placehold.co/800x600/FFD700/000000/png?text=GLI+City+Hotel',
            'is_featured': True,
            'tags': ['도심', '비즈니스', '서울', '편리', 'City', 'Business', 'Seoul', 'Convenient'],
            'attributes': {
                'location': 'Seoul, Korea',
                'location_en': 'Seoul, Korea',
                'rating': 5,
                'rooms': [
                    {
                        'type': 'standard',
                        'type_ko': '스탠다드',
                        'price': 180,
                        'features': ['City View', 'Business Center', 'Gym Access'],
                        'features_ko': ['시티 뷰', '비즈니스 센터', '헬스장 이용']
                    },
                    {
                        'type': 'deluxe',
                        'type_ko': '디럭스',
                        'price': 280,
                        'features': ['Han River View', 'Executive Lounge', 'Express Check-in'],
                        'features_ko': ['한강 뷰', '이그제큐티브 라운지', '빠른 체크인']
                    },
                    {
                        'type': 'suite',
                        'type_ko': '스위트',
                        'price': 500,
                        'features': ['Presidential Suite', 'Private Elevator', 'Personal Assistant', 'Rooftop Access'],
                        'features_ko': ['프레지덴셜 스위트', '전용 엘리베이터', '개인 비서', '루프탑 이용']
                    }
                ]
            },
        },
    ]

    for data in resorts_data:
        product, created = ShoppingProduct.objects.get_or_create(
            category=category,
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"  ✅ 리조트 생성: {product.name}")
        else:
            print(f"  ⏭️  리조트 존재: {product.name}")


def create_goods_products(category):
    """상품 생성"""
    goods_data = [
        {
            'name': 'GLI Premium 후드티',
            'name_en': 'GLI Premium Hoodie',
            'description': '프리미엄 코튼 소재의 GLI 브랜드 후드티입니다. 부드럽고 따뜻한 착용감과 세련된 디자인이 특징입니다.',
            'description_en': 'GLI brand hoodie made of premium cotton. Features soft, warm comfort and sophisticated design.',
            'short_description': 'GLI 브랜드 프리미엄 코튼 후드티',
            'short_description_en': 'GLI Brand Premium Cotton Hoodie',
            'product_type': 'goods',
            'price_glil': Decimal('89.99'),
            'price_usd': Decimal('89.99'),
            'stock_quantity': 15,
            'main_image_url': 'https://placehold.co/400x500/000000/D4AF37/png?text=GLI+Hoodie',
            'is_featured': True,
            'tags': ['패션', '의류', '후드티', '프리미엄', 'Fashion', 'Clothing', 'Hoodie', 'Premium'],
            'attributes': {
                'categoryId': 'fashion',
                'sizes': ['S', 'M', 'L', 'XL'],
                'colors': ['Black', 'Navy', 'Gray'],
                'material': 'Premium Cotton',
                'salePercent': 25,
                'originalPrice': 120.00
            },
        },
        {
            'name': 'GLI Signature 모자',
            'name_en': 'GLI Signature Cap',
            'description': 'GLI 로고가 새겨진 시그니처 캡입니다. 어떤 스타일에도 잘 어울리는 베이직한 디자인입니다.',
            'description_en': 'Signature cap with GLI logo. Basic design that goes well with any style.',
            'short_description': 'GLI 로고 시그니처 캡',
            'short_description_en': 'GLI Logo Signature Cap',
            'product_type': 'goods',
            'price_glil': Decimal('35.50'),
            'price_usd': Decimal('35.50'),
            'stock_quantity': 8,
            'main_image_url': 'https://placehold.co/400x400/FFFFFF/000000/png?text=GLI+Cap',
            'is_featured': False,
            'tags': ['액세서리', '모자', '캡', 'Accessories', 'Hat', 'Cap'],
            'attributes': {
                'categoryId': 'accessories',
                'colors': ['Black', 'White', 'Navy'],
                'adjustable': True
            },
        },
        {
            'name': 'GLI 무선 이어폰',
            'name_en': 'GLI Wireless Earphones',
            'description': '고음질 GLI 브랜드 블루투스 이어폰입니다. 최신 노이즈 캔슬링 기술과 긴 배터리 수명을 자랑합니다.',
            'description_en': 'High-quality GLI brand Bluetooth earphones. Features latest noise canceling technology and long battery life.',
            'short_description': '고음질 블루투스 이어폰',
            'short_description_en': 'High-Quality Bluetooth Earphones',
            'product_type': 'goods',
            'price_glil': Decimal('149.99'),
            'price_usd': Decimal('149.99'),
            'stock_quantity': 12,
            'main_image_url': 'https://placehold.co/400x400/1E90FF/FFFFFF/png?text=GLI+Earphones',
            'is_featured': True,
            'tags': ['전자기기', '이어폰', '블루투스', 'Electronics', 'Earphones', 'Bluetooth'],
            'attributes': {
                'categoryId': 'electronics',
                'batteryLife': '24 hours',
                'noiseCanceling': True,
                'waterproof': 'IPX4',
                'salePercent': 25,
                'originalPrice': 199.99
            },
        },
        {
            'name': 'GLI 텀블러',
            'name_en': 'GLI Tumbler',
            'description': '보온/보냉 기능이 있는 GLI 브랜드 텀블러입니다. 스테인레스 스틸 소재로 오래도록 사용할 수 있습니다.',
            'description_en': 'GLI brand tumbler with heat/cold retention. Made of stainless steel for long-lasting use.',
            'short_description': '보온/보냉 스테인레스 텀블러',
            'short_description_en': 'Heat/Cold Retention Stainless Tumbler',
            'product_type': 'goods',
            'price_glil': Decimal('25.00'),
            'price_usd': Decimal('25.00'),
            'stock_quantity': 20,
            'main_image_url': 'https://placehold.co/300x500/C0C0C0/000000/png?text=GLI+Tumbler',
            'is_featured': False,
            'tags': ['라이프스타일', '텀블러', '스테인레스', 'Lifestyle', 'Tumbler', 'Stainless'],
            'attributes': {
                'categoryId': 'lifestyle',
                'capacity': '500ml',
                'material': 'Stainless Steel',
                'colors': ['Silver', 'Black', 'Gold']
            },
        },
        {
            'name': 'GLI 요가매트',
            'name_en': 'GLI Yoga Mat',
            'description': '프리미엄 친환경 소재 요가매트입니다. 미끄럼 방지 기능과 쿠션감이 뛰어나 편안한 운동을 즐길 수 있습니다.',
            'description_en': 'Premium eco-friendly yoga mat. Excellent anti-slip function and cushioning for comfortable exercise.',
            'short_description': '친환경 프리미엄 요가매트',
            'short_description_en': 'Eco-Friendly Premium Yoga Mat',
            'product_type': 'goods',
            'price_glil': Decimal('75.00'),
            'price_usd': Decimal('75.00'),
            'stock_quantity': 6,
            'main_image_url': 'https://placehold.co/600x400/9370DB/FFFFFF/png?text=GLI+Yoga+Mat',
            'is_featured': False,
            'tags': ['스포츠', '요가', '매트', '운동', 'Sports', 'Yoga', 'Mat', 'Exercise'],
            'attributes': {
                'categoryId': 'sports',
                'thickness': '6mm',
                'material': 'TPE (Eco-Friendly)',
                'size': '183cm x 61cm',
                'colors': ['Purple', 'Pink', 'Blue', 'Green']
            },
        },
        {
            'name': 'GLI 디퓨저',
            'name_en': 'GLI Diffuser',
            'description': 'GLI 시그니처 향이 나는 아로마 디퓨저입니다. 고급스러운 디자인과 은은한 향으로 공간을 채워줍니다.',
            'description_en': 'Aroma diffuser with GLI signature scent. Fills the space with luxurious design and subtle fragrance.',
            'short_description': 'GLI 시그니처 향 아로마 디퓨저',
            'short_description_en': 'GLI Signature Scent Aroma Diffuser',
            'product_type': 'goods',
            'price_glil': Decimal('95.00'),
            'price_usd': Decimal('95.00'),
            'stock_quantity': 0,
            'main_image_url': 'https://placehold.co/400x500/FFD700/000000/png?text=GLI+Diffuser',
            'is_featured': False,
            'tags': ['홈&리빙', '디퓨저', '향', '인테리어', 'Home', 'Diffuser', 'Fragrance', 'Interior'],
            'attributes': {
                'categoryId': 'home',
                'capacity': '200ml',
                'scents': ['Lavender', 'Ocean Breeze', 'Forest'],
                'duration': '60 days'
            },
        },
        {
            'name': 'GLI 스마트워치',
            'name_en': 'GLI Smart Watch',
            'description': 'GLI 브랜딩이 적용된 스마트워치입니다. 건강 관리와 스마트 기능이 완벽하게 조화를 이룹니다.',
            'description_en': 'Smart watch with GLI branding. Perfect harmony of health management and smart features.',
            'short_description': 'GLI 브랜딩 스마트워치',
            'short_description_en': 'GLI Branding Smart Watch',
            'product_type': 'goods',
            'price_glil': Decimal('299.99'),
            'price_usd': Decimal('299.99'),
            'stock_quantity': 5,
            'main_image_url': 'https://placehold.co/400x400/000000/1E90FF/png?text=GLI+Watch',
            'is_featured': True,
            'tags': ['전자기기', '스마트워치', '웨어러블', 'Electronics', 'Smart Watch', 'Wearable'],
            'attributes': {
                'categoryId': 'electronics',
                'batteryLife': '5 days',
                'waterproof': '5ATM',
                'features': ['Heart Rate Monitor', 'GPS', 'Sleep Tracking', 'Notification'],
                'compatibility': ['iOS', 'Android']
            },
        },
        {
            'name': 'GLI 레더 지갑',
            'name_en': 'GLI Leather Wallet',
            'description': '프리미엄 가죽으로 제작된 GLI 지갑입니다. 실용적인 디자인과 고급스러운 마감이 특징입니다.',
            'description_en': 'GLI wallet made of premium leather. Features practical design and luxurious finish.',
            'short_description': '프리미엄 가죽 지갑',
            'short_description_en': 'Premium Leather Wallet',
            'product_type': 'goods',
            'price_glil': Decimal('128.00'),
            'price_usd': Decimal('128.00'),
            'stock_quantity': 10,
            'main_image_url': 'https://placehold.co/400x300/8B4513/FFFFFF/png?text=GLI+Wallet',
            'is_featured': False,
            'tags': ['액세서리', '지갑', '가죽', 'Accessories', 'Wallet', 'Leather'],
            'attributes': {
                'categoryId': 'accessories',
                'material': 'Genuine Leather',
                'colors': ['Black', 'Brown', 'Navy'],
                'cardSlots': 8,
                'salePercent': 20,
                'originalPrice': 160.00
            },
        },
    ]

    for data in goods_data:
        product, created = ShoppingProduct.objects.get_or_create(
            category=category,
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"  ✅ 상품 생성: {product.name}")
        else:
            print(f"  ⏭️  상품 존재: {product.name}")


def create_restaurant_products(category):
    """레스토랑 상품 생성"""
    restaurants_data = [
        {
            'name': 'GLI Fine Dining Seoul',
            'name_en': 'GLI Fine Dining Seoul',
            'description': '서울 강남에 위치한 프렌치 파인 다이닝 레스토랑입니다. 미슐랭 스타 셰프가 선보이는 혁신적인 요리를 경험하세요.',
            'description_en': 'French fine dining restaurant located in Gangnam, Seoul. Experience innovative cuisine by Michelin star chef.',
            'short_description': '미슐랭 스타 프렌치 파인 다이닝',
            'short_description_en': 'Michelin Star French Fine Dining',
            'product_type': 'restaurant',
            'price_glil': Decimal('200.00'),
            'price_usd': Decimal('200.00'),
            'stock_quantity': 30,
            'main_image_url': 'https://placehold.co/800x600/800020/FFFFFF/png?text=GLI+Fine+Dining',
            'is_featured': True,
            'tags': ['파인다이닝', '프렌치', '미슐랭', '강남', 'Fine Dining', 'French', 'Michelin', 'Gangnam'],
            'attributes': {
                'location': 'Gangnam, Seoul',
                'location_en': 'Gangnam, Seoul',
                'cuisine': 'French',
                'michelin_stars': 2,
                'price_range': '₩₩₩₩',
                'dress_code': 'Business Casual',
                'business_hours': {
                    'lunch': '12:00 - 15:00',
                    'dinner': '18:00 - 22:00'
                },
                'courses': [
                    {
                        'name': '런치 코스',
                        'name_en': 'Lunch Course',
                        'price': 150,
                        'description': '5코스 런치 메뉴',
                        'description_en': '5-course lunch menu'
                    },
                    {
                        'name': '디너 코스',
                        'name_en': 'Dinner Course',
                        'price': 200,
                        'description': '7코스 디너 메뉴',
                        'description_en': '7-course dinner menu'
                    },
                    {
                        'name': '시그니처 코스',
                        'name_en': 'Signature Course',
                        'price': 350,
                        'description': '10코스 시그니처 메뉴',
                        'description_en': '10-course signature menu'
                    }
                ]
            },
        },
        {
            'name': 'GLI Japanese Omakase',
            'name_en': 'GLI Japanese Omakase',
            'description': '청담동에 위치한 정통 일식 오마카세 레스토랑입니다. 당일 공수한 신선한 재료로 최고의 스시를 선보입니다.',
            'description_en': 'Authentic Japanese omakase restaurant in Cheongdam-dong. Presents the finest sushi with fresh ingredients delivered daily.',
            'short_description': '정통 일식 오마카세',
            'short_description_en': 'Authentic Japanese Omakase',
            'product_type': 'restaurant',
            'price_glil': Decimal('250.00'),
            'price_usd': Decimal('250.00'),
            'stock_quantity': 20,
            'main_image_url': 'https://placehold.co/800x600/DC143C/FFFFFF/png?text=GLI+Omakase',
            'is_featured': True,
            'tags': ['일식', '오마카세', '스시', '청담동', 'Japanese', 'Omakase', 'Sushi', 'Cheongdam'],
            'attributes': {
                'location': 'Cheongdam-dong, Seoul',
                'location_en': 'Cheongdam-dong, Seoul',
                'cuisine': 'Japanese',
                'seating': 'Counter only (12 seats)',
                'price_range': '₩₩₩₩₩',
                'reservations': 'Required',
                'business_hours': {
                    'lunch': 'By reservation only',
                    'dinner': '18:00 - 22:00'
                },
                'courses': [
                    {
                        'name': '스탠다드 오마카세',
                        'name_en': 'Standard Omakase',
                        'price': 250,
                        'description': '15피스 니기리',
                        'description_en': '15-piece nigiri'
                    },
                    {
                        'name': '프리미엄 오마카세',
                        'name_en': 'Premium Omakase',
                        'price': 400,
                        'description': '20피스 니기리 + 특선 요리',
                        'description_en': '20-piece nigiri + special dishes'
                    }
                ]
            },
        },
        {
            'name': 'GLI Italian Trattoria',
            'name_en': 'GLI Italian Trattoria',
            'description': '이태원에 위치한 정통 이탈리안 트라토리아입니다. 전통 레시피와 신선한 재료로 진정한 이탈리아의 맛을 선사합니다.',
            'description_en': 'Authentic Italian trattoria in Itaewon. Delivers true Italian taste with traditional recipes and fresh ingredients.',
            'short_description': '정통 이탈리안 트라토리아',
            'short_description_en': 'Authentic Italian Trattoria',
            'product_type': 'restaurant',
            'price_glil': Decimal('120.00'),
            'price_usd': Decimal('120.00'),
            'stock_quantity': 40,
            'main_image_url': 'https://placehold.co/800x600/008000/FFFFFF/png?text=GLI+Trattoria',
            'is_featured': True,
            'tags': ['이탈리안', '파스타', '피자', '이태원', 'Italian', 'Pasta', 'Pizza', 'Itaewon'],
            'attributes': {
                'location': 'Itaewon, Seoul',
                'location_en': 'Itaewon, Seoul',
                'cuisine': 'Italian',
                'ambiance': 'Casual',
                'price_range': '₩₩₩',
                'business_hours': {
                    'lunch': '11:30 - 15:00',
                    'dinner': '17:30 - 22:00'
                },
                'specialties': [
                    'Handmade Pasta',
                    'Wood-fired Pizza',
                    'Tiramisu'
                ],
                'menu_highlights': [
                    {
                        'name': '트러플 파스타',
                        'name_en': 'Truffle Pasta',
                        'price': 45
                    },
                    {
                        'name': '마르게리타 피자',
                        'name_en': 'Margherita Pizza',
                        'price': 28
                    },
                    {
                        'name': '오쏘부코',
                        'name_en': 'Osso Buco',
                        'price': 55
                    }
                ]
            },
        },
    ]

    for data in restaurants_data:
        product, created = ShoppingProduct.objects.get_or_create(
            category=category,
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"  ✅ 레스토랑 생성: {product.name}")
        else:
            print(f"  ⏭️  레스토랑 존재: {product.name}")


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("GLI-L 코인 쇼핑몰 초기 데이터 생성")
    print("=" * 80)
    print()

    # 카테고리 생성
    print("📁 카테고리 생성 중...")
    categories = create_categories()
    print()

    # 리조트 상품 생성
    print("🏨 리조트 & 호텔 상품 생성 중...")
    create_resort_products(categories['resort'])
    print()

    # 일반 상품 생성
    print("🛍️  일반 상품 생성 중...")
    create_goods_products(categories['products'])
    print()

    # 레스토랑 상품 생성
    print("🍽️  레스토랑 상품 생성 중...")
    create_restaurant_products(categories['restaurant'])
    print()

    # 완료 통계
    print("=" * 80)
    print("✅ 초기 데이터 생성 완료!")
    print("=" * 80)
    print(f"📊 통계:")
    print(f"  - 카테고리: {ShoppingCategory.objects.count()}개")
    print(f"  - 상품: {ShoppingProduct.objects.count()}개")
    print(f"    - 리조트: {ShoppingProduct.objects.filter(product_type='resort').count()}개")
    print(f"    - 일반 상품: {ShoppingProduct.objects.filter(product_type='goods').count()}개")
    print(f"    - 레스토랑: {ShoppingProduct.objects.filter(product_type='restaurant').count()}개")
    print()


if __name__ == '__main__':
    main()
