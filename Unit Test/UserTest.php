<?php

namespace Tests\Unit;

use App\Actions\Fortify\CreateNewUser;
use App\Actions\Fortify\UpdateUserPassword;
use App\Actions\Jetstream\DeleteUser;
use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Storage;
use Laravel\Jetstream\Jetstream;
use Tests\TestCase;

class UserTest extends TestCase
{
    use DatabaseTransactions;
    protected $cus = 'congdanhabc@outlook.com.vn';
    protected $admin = 'ncongdanh91@gmail.com';
    protected function authenticate($email_user)
    {
        $user = User::where('email', $email_user)->first();
        if (!$user) {
            $this->markTestSkipped('User not found for testing.');
        }

        $this->actingAs($user);
        return $user;
    }
    public function test_Create_User()
    {
        $input = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password',
            'password_confirmation' => 'password',
            'terms' => Jetstream::hasTermsAndPrivacyPolicyFeature(),
        ];

        $user = (new CreateNewUser())->create($input);
        $this->assertDatabaseHas('users', [
            'name' => $input['name'],
            'email' => $input['email'],
        ]);
        $this->assertTrue(Hash::check($input['password'], $user->password));
    }

    public function test_Delete_User()
    {
        $user = $this->authenticate($this->cus);

        $this->assertDatabaseHas('users', [
            'name' => $user->name,
            'email' => $user->email,
        ]);

        (new DeleteUser())->delete($user);

        $this->assertDatabaseMissing('users', ['email' => 'congdanhabc@outlook.com.vn']);
    }

    public function test_update_password()
    {
        $user = $this->authenticate($this->cus);
        $this->assertTrue(Hash::check('congdanh2003', $user->password));

        //Gọi hàm update với dữ liệu đầu vào.
        $input = [
            'current_password' => 'congdanh2003',
            'password' => 'new_pass',
            'password_confirmation' => 'new_pass',
        ];

        (new UpdateUserPassword())->update($user, $input);

        //Kiểm tra mật khẩu đã được cập nhật.
        $updatedUser = User::find($user->id);
        $this->assertTrue(Hash::check('new_pass', $updatedUser->password));
    }
    public function test_add_admin_process()
    {
        $user = $this->authenticate($this->admin);

        Storage::fake('public'); // Use fake storage for testing file uploads

        $request = [
            'name' => 'Test Admin',
            'email' => 'test@example.com',
            'phone' => '1234567890',
            'type' => '3', // Sub Admin
            'salary' => 1000,
            'password' => 'testpassword123',
            'confirm_password' => 'testpassword123',
            'image' => UploadedFile::fake()->image('test.jpg'), // Create a fake image upload
        ];

        $response = $this->post(route('/admin-add-process'), $request);

        $response->assertSessionHas('success', 'Admin added successfully !');


        $this->assertDatabaseHas('users', [
            'name' => 'Test Admin',
            'email' => 'test@example.com',
            'phone' => '1234567890',
            'usertype' => '3',
            'salary' => 1000,
        ]);
    }
}
//./vendor/bin/phpunit tests/Unit/UserTest.php --filter test_add_admin_process
